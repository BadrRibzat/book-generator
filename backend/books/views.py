# books/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import FileResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import os
import json
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

from .models import Book, BookTemplate, Domain, Niche, BookStyle, CoverStyle
from .serializers import (
    BookSerializer, 
    BookCreateSerializer, 
    BookStatusSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    DomainSerializer,
    NicheSerializer,
    BookStyleSerializer,
    CoverStyleSerializer
)
from .services.book_generator import BookGeneratorProfessional
from .tasks import generate_book_content, generate_book_covers, create_final_book_pdf
from .services.pdf_merger import PDFMerger
from covers.services import CoverGeneratorProfessional
from backend.utils.mongodb import get_mongodb_db


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_guided_book(request):
    """
    Create book using the guided workflow with domain, niche, style, cover_style
    """
    serializer = BookCreateSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    book = serializer.save()
    
    # Trigger async content generation
    try:
        # Trigger the Celery task for content generation
        generate_book_content.delay(book.id)
        print(f"Triggered async content generation for book {book.id}")
    except Exception as e:
        book.status = 'error'
        book.error_message = f"Failed to start content generation: {str(e)}"
        book.save()
    
    # Return full book data including ID
    response_data = BookSerializer(book).data
    return Response(
        response_data,
        status=status.HTTP_201_CREATED
    )


class DomainViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for reading domains
    """
    queryset = Domain.objects.filter(is_active=True)
    serializer_class = DomainSerializer
    permission_classes = [AllowAny]


class NicheViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for reading niches, filtered by domain
    """
    serializer_class = NicheSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Niche.objects.filter(is_active=True)
        domain_slug = self.request.query_params.get('domain', None)
        if domain_slug is not None:
            queryset = queryset.filter(domain__slug=domain_slug)
        return queryset


class BookStyleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for reading book styles
    """
    queryset = BookStyle.objects.filter(is_active=True)
    serializer_class = BookStyleSerializer
    permission_classes = [AllowAny]


class CoverStyleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for reading cover styles
    """
    queryset = CoverStyle.objects.filter(is_active=True)
    serializer_class = CoverStyleSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer
        return BookSerializer
    
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new book and return full book data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        
        # Trigger async content generation
        self._generate_book_content(book)
        
        # Return full book data using BookSerializer
        response_serializer = BookSerializer(book)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Get book generation status and progress
        """
        book = self.get_object()
        serializer = BookStatusSerializer(book)
        return Response(serializer.data)
    
    def _generate_book_content(self, book):
        """
        Trigger async book content generation using Celery
        """
        try:
            # Trigger the Celery task for content generation
            generate_book_content.delay(book.id)
            print(f"Triggered async content generation for book {book.id}")

        except Exception as e:
            book.status = 'error'
            book.error_message = f"Failed to start content generation: {str(e)}"
            book.save()
    
    def _generate_covers(self, book):
        """
        Trigger async cover generation using Celery
        """
        try:
            # Trigger the Celery task for cover generation
            generate_book_covers.delay(book.id)
            print(f"Triggered async cover generation for book {book.id}")

        except Exception as e:
            print(f"Failed to start cover generation: {str(e)}")
            book.status = 'error'
            book.error_message = f"Cover generation failed: {str(e)}"
            book.save()
    
    @action(detail=True, methods=['post'])
    def regenerate_covers(self, request, pk=None):
        """
        Regenerate all 3 cover options
        """
        book = self.get_object()
        
        # Allow regenerating covers even if in error state
        if book.status not in ['content_generated', 'cover_pending', 'ready', 'error']:
            return Response(
                {'error': 'Content must be generated first'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete old covers
        book.covers.all().delete()
        
        # Set status to indicate we're working on covers
        book.status = 'content_generated'
        book.error_message = None
        book.save()
        
        # Generate new ones
        self._generate_covers(book)
        
        return Response(BookSerializer(book).data)
    
    @action(detail=True, methods=['post'])
    def select_cover(self, request, pk=None):
        """
        Step 2: User selects a cover (required before download)
        """
        book = self.get_object()
        cover_id = request.data.get('cover_id')
        
        if not cover_id:
            return Response(
                {'error': 'cover_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            print(f"Selecting cover {cover_id} for book {book.id}")
            
            # Check if the cover exists
            try:
                cover = book.covers.get(id=cover_id)
            except Exception as e:
                print(f"Cover lookup failed: {str(e)}")
                return Response(
                    {'error': f'Cover not found: {str(e)}'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            # Check if cover image exists
            from pathlib import Path
            from django.conf import settings
            image_path = Path(settings.MEDIA_ROOT) / cover.image_path
            if not image_path.exists():
                print(f"Warning: Cover image file does not exist: {image_path}")
            
            # Select the cover
            try:
                cover.select()  # This also updates book status to 'ready'
                print(f"Cover {cover_id} selected successfully")
            except Exception as e:
                print(f"Cover selection failed: {str(e)}")
                return Response(
                    {'error': f'Cover selection failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Generate final PDF using Celery task
            try:
                create_final_book_pdf.delay(book.id)
                print(f"Triggered async final PDF creation for book {book.id}")
            except Exception as e:
                print(f"Failed to start PDF creation: {str(e)}")
                return Response(
                    {'error': f'PDF creation failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(BookSerializer(book).data)
            
        except Exception as e:
            print(f"Cover selection overall error: {str(e)}")
            return Response(
                {'error': f'Cover selection failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download the final PDF of a completed book
        """
        book = self.get_object()
        
        if not book.can_download():
            return Response(
                {'error': 'Book is not ready for download. Please ensure a cover is selected and the book is completed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get final PDF path from MongoDB
            db = get_mongodb_db()
            content_doc = db.book_contents.find_one({'book_id': book.id})
            
            if not content_doc:
                return Response(
                    {'error': 'Book content not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            final_pdf_path = content_doc.get('final_pdf_path')
            if not final_pdf_path:
                return Response(
                    {'error': 'Final PDF not found. Please select a cover first.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check if file exists
            from pathlib import Path
            pdf_path = Path(final_pdf_path)
            if not pdf_path.exists():
                return Response(
                    {'error': 'PDF file not found on server'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Record download for analytics
            book.record_download(request)
            
            # Return file response
            response = FileResponse(
                open(pdf_path, 'rb'),
                content_type='application/pdf',
                filename=f"{book.title}.pdf"
            )
            response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
            
            return response
            
        except Exception as e:
            print(f"Download error for book {book.id}: {str(e)}")
            return Response(
                {'error': f'Download failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _create_final_pdf(self, book):
        """
        Merge cover + interior into final downloadable PDF
        """
        try:
            # Get interior PDF path from MongoDB
            db = get_mongodb_db()
            content_doc = db.book_contents.find_one({'book_id': book.id})
            
            if not content_doc:
                print(f"No content found for book {book.id} in MongoDB")
                # Try to regenerate content if missing
                print(f"Attempting to regenerate content for book {book.id}")
                self._generate_book_content(book)
                # Try to fetch again
                content_doc = db.book_contents.find_one({'book_id': book.id})
                if not content_doc:
                    raise Exception("Book content could not be generated")
            
            interior_pdf_path = content_doc.get('interior_pdf_path')
            if not interior_pdf_path:
                raise Exception("Interior PDF path not found in content document")
            
            # Check if interior PDF file exists
            from pathlib import Path
            if not Path(interior_pdf_path).exists():
                print(f"Interior PDF file not found at: {interior_pdf_path}")
                # Try to regenerate the PDF
                generator = BookGeneratorProfessional()
                content_data = content_doc.get('content', {})
                if content_data:
                    interior_pdf_path = generator.create_pdf(book, content_data)
                    # Update MongoDB with new path
                    db.book_contents.update_one(
                        {'book_id': book.id},
                        {'$set': {'interior_pdf_path': interior_pdf_path}}
                    )
                else:
                    raise Exception("No content data available to regenerate PDF")
            
            # Merge with selected cover
            merger = PDFMerger()
            final_pdf_path = merger.merge_book(
                book, 
                interior_pdf_path, 
                book.selected_cover
            )
            
            # Update MongoDB with final path
            db.book_contents.update_one(
                {'book_id': book.id},
                {'$set': {'final_pdf_path': final_pdf_path}}
            )
            
            # Update book model
            book.final_pdf_path = final_pdf_path
            book.status = 'ready'
            book.save()
            
        except Exception as e:
            print(f"Final PDF creation failed for book {book.id}: {str(e)}")
            book.status = 'error'
            book.error_message = f"PDF creation failed: {str(e)}"
            book.save()
            raise
    
    @action(detail=True, methods=['post'])
    def regenerate_content(self, request, pk=None):
        """
        Regenerate book content (keeps same config)
        """
        book = self.get_object()
        
        # Reset book status
        book.status = 'draft'
        book.error_message = None
        book.save()
        
        # Delete old covers
        book.covers.all().delete()
        
        # Regenerate content
        self._generate_book_content(book)
        
        return Response(BookSerializer(book).data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get user's book history
        """
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def clear_history(self, request):
        """
        Delete all user's books
        """
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Authentication views

@extend_schema(
    tags=['Authentication'],
    summary='Register new user (SignUp)',
    description='''
    Create a new user account and automatically log them in.
    
    **Flow:** SignUp → SignIn (automatic) → Profile
    
    Returns user data and session cookie for authentication.
    ''',
    request=UserRegistrationSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description='Validation errors (passwords don\'t match, username taken, etc.)')
    },
    examples=[
        OpenApiExample(
            'SignUp Example',
            value={
                'username': 'johndoe',
                'email': 'john@example.com',
                'password': 'securepass123',
                'password2': 'securepass123'
            },
            request_only=True
        )
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create user profile
        from users.models import UserProfile
        UserProfile.objects.create(user=user)
        
        # Don't auto-login after registration - user must sign in separately
        return Response(
            {
                'user': UserSerializer(user).data,
                'message': 'Registration successful. Please sign in with your credentials.'
            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Authentication'],
    summary='Login user (SignIn)',
    description='''
    Authenticate user with username and password.
    
    **Flow:** SignUp → SignIn → Profile
    
    Returns user data and session cookie for subsequent requests.
    ''',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'johndoe'},
                'password': {'type': 'string', 'example': 'securepass123'}
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: UserSerializer,
        400: OpenApiResponse(description='Missing username or password'),
        401: OpenApiResponse(description='Invalid credentials')
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user with username and password"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request=request, username=username, password=password)
    
    if user:
        login(request, user)
        
        # Force session save
        request.session.save()
        
        # Debug: Print session info
        print(f"Login successful for user: {user.username}")
        print(f"Session key: {request.session.session_key}")
        print(f"Session data: {dict(request.session)}")
        print(f"Session modified: {request.session.modified}")
        
        response = Response({
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        })
        
        # Don't manually set cookie - Django middleware handles it
        # The session cookie should be set automatically by SessionMiddleware
        
        return response
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@extend_schema(
    tags=['Authentication'],
    summary='Logout user (SignOut)',
    description='''
    Logout current user and invalidate session.
    
    **Flow:** Profile → SignOut → SignIn
    ''',
    responses={
        200: OpenApiResponse(description='Logout successful'),
        401: OpenApiResponse(description='Not authenticated')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout current user"""
    logout(request)
    return Response({'message': 'Logout successful'})


@extend_schema(
    tags=['Authentication'],
    summary='Get current user profile',
    description='''
    Get profile information for the currently authenticated user.
    
    **Flow:** SignUp/SignIn → Profile
    
    Use this to check authentication status and get user details.
    ''',
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description='Not authenticated')
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@method_decorator(csrf_exempt, name='dispatch')
def current_user(request):
    """Get current user info"""
    # Debug: Print session and auth info
    print(f"\n=== Current User Request Debug ===")
    print(f"Request path: {request.path}")
    print(f"Request method: {request.method}")
    print(f"Session key from session: {request.session.session_key}")
    print(f"Session key from cookie: {request.COOKIES.get(settings.SESSION_COOKIE_NAME, 'NOT FOUND')}")
    print(f"User: {request.user}")
    print(f"User ID: {request.user.id if request.user.is_authenticated else 'N/A'}")
    print(f"Is authenticated: {request.user.is_authenticated}")
    print(f"Session data: {dict(request.session)}")
    print(f"Session exists: {request.session.session_key is not None}")
    print(f"All cookies: {dict(request.COOKIES)}")
    print(f"Session age: {request.session.get_expiry_age()}")
    print(f"Session expiry date: {request.session.get_expiry_date()}")
    print(f"=================================\n")
    
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response(UserSerializer(request.user).data)


