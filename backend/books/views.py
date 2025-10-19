# books/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import FileResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.conf import settings
from pathlib import Path
import os
import json
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

from .models import Book
from .serializers import (
    BookSerializer, 
    BookCreateSerializer, 
    UserSerializer,
    UserRegistrationSerializer
)
from .services.book_generator import BookGenerator
from .services.pdf_merger import PDFMerger
from covers.services import CoverGenerator
from backend.utils.mongodb import get_mongodb_db

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
    
    def create(self, request):
        """
        Step 1: Create book and start content generation
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        
        # Trigger async content generation
        self._generate_book_content(book)
        
        # Return full book data including ID
        response_data = BookSerializer(book).data
        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )
    
    def _generate_book_content(self, book):
        """
        Generate book content and update status
        This should ideally be an async task (Celery/Django-Q)
        For now, we'll do it synchronously with error handling
        """
        try:
            book.status = 'generating'
            book.save()
            
            # Generate content using Groq
            generator = BookGenerator()
            content_data = generator.generate_book_content(book)
            
            # Create PDF
            interior_pdf_path = generator.create_pdf(book, content_data)
            
            # Store content in MongoDB
            db = get_mongodb_db()
            result = db.book_contents.insert_one({
                'book_id': book.id,
                'content': content_data,
                'interior_pdf_path': interior_pdf_path,
                'created_at': timezone.now().isoformat()
            })
            
            book.mongodb_id = str(result.inserted_id)
            book.status = 'content_generated'
            book.content_generated_at = timezone.now()
            book.save()
            
            # Auto-trigger cover generation
            self._generate_covers(book)
            
        except Exception as e:
            book.status = 'error'
            book.error_message = str(e)
            book.save()
    
    def _generate_covers(self, book):
        """
        Generate 3 cover options for the book
        """
        try:
            # First check if MongoDB connection is valid
            try:
                db = get_mongodb_db()
                content_doc = db.book_contents.find_one({'book_id': book.id})
                if not content_doc:
                    raise Exception("Book content not found in MongoDB")
            except Exception as mongo_err:
                print(f"MongoDB connection error: {mongo_err}")
                raise Exception(f"Database connection error: {str(mongo_err)}")
            
            print(f"Generating covers for book {book.id}: {book.title}")
            cover_gen = CoverGenerator()
            covers = cover_gen.generate_three_covers(book)
            
            # Check if covers were successfully generated
            if len(covers) == 0:
                raise Exception("No covers were generated")
                
            print(f"Successfully generated {len(covers)} covers for book {book.id}")
            book.status = 'content_generated'  # Change to content_generated to force cover selection
            book.save()
            
        except Exception as e:
            print(f"Cover generation failed: {str(e)}")
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
            
            # Generate final PDF
            try:
                self._create_final_pdf(book)
                print(f"Final PDF created for book {book.id}")
            except Exception as e:
                print(f"PDF creation failed: {str(e)}")
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
    
    def _create_final_pdf(self, book):
        """
        Merge cover + interior into final downloadable PDF
        """
        try:
            # Get interior PDF path from MongoDB
            db = get_mongodb_db()
            content_doc = db.book_contents.find_one({'book_id': book.id})
            
            if not content_doc:
                raise Exception("Book content not found")
            
            interior_pdf_path = content_doc['interior_pdf_path']
            
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
            
        except Exception as e:
            book.status = 'error'
            book.error_message = f"PDF merge failed: {str(e)}"
            book.save()
            raise
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Step 3: Download final book (only if cover is selected)
        """
        book = self.get_object()
        
        if not book.can_download():
            return Response(
                {'error': 'Book not ready. Please select a cover first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get final PDF path from MongoDB
        db = get_mongodb_db()
        content_doc = db.book_contents.find_one({'book_id': book.id})
        
        if not content_doc or 'final_pdf_path' not in content_doc:
            return Response(
                {'error': 'Final PDF not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serve the file
        pdf_path = Path(settings.MEDIA_ROOT) / content_doc['final_pdf_path']
        
        if not pdf_path.exists():
            raise Http404("PDF file not found")
        
        response = FileResponse(
            open(pdf_path, 'rb'),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
        
        return response
    
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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sub_niches(request):
    """
    Get available sub-niches organized by domain
    
    Returns trending categories with built-in audiences:
    - Language and Kids (3 niches)
    - Technology and AI (3 niches)
    - Nutrition and Wellness (3 niches)
    - Meditation (3 niches)
    - Home Workout (3 niches)
    """
    niches = {
        'language_kids': [
            {'value': 'ai_learning_stories', 'label': 'AI-Powered Personalized Learning Stories'},
            {'value': 'multilingual_coloring', 'label': 'Multilingual Coloring Books'},
            {'value': 'kids_mindful_journals', 'label': 'Kids\' Mindful Activity Journals'},
        ],
        'tech_ai': [
            {'value': 'ai_ethics', 'label': 'AI Ethics and Future Trends'},
            {'value': 'nocode_guides', 'label': 'No-Code/Low-Code Development Guides'},
            {'value': 'smart_home_diy', 'label': 'DIY Smart Home and Automation'},
        ],
        'nutrition': [
            {'value': 'specialty_diet', 'label': 'Specialty Diet Cookbooks'},
            {'value': 'plant_based_cooking', 'label': 'Plant-Based Cooking for Beginners'},
            {'value': 'nutrition_mental_health', 'label': 'Nutrition for Mental Health'},
        ],
        'meditation': [
            {'value': 'mindfulness_anxiety', 'label': 'Mindfulness and Anxiety Workbooks'},
            {'value': 'sleep_meditation', 'label': 'Sleep Meditation Stories'},
            {'value': 'gratitude_journals', 'label': 'Daily Gratitude Journals with Prompts'},
        ],
        'home_workout': [
            {'value': 'equipment_free', 'label': 'Equipment-Free Workout Plans'},
            {'value': 'yoga_remote_workers', 'label': 'Yoga and Stretching for Remote Workers'},
            {'value': 'mobility_training', 'label': 'Beginner\'s Mobility Training'},
        ],
    }
    
    domains = [
        {'value': 'language_kids', 'label': 'Language and Kids'},
        {'value': 'tech_ai', 'label': 'Technology and AI'},
        {'value': 'nutrition', 'label': 'Nutrition and Wellness'},
        {'value': 'meditation', 'label': 'Meditation'},
        {'value': 'home_workout', 'label': 'Home Workout'},
    ]
    
    return Response({
        'domains': domains,
        'sub_niches': niches,
        'page_lengths': [15, 20, 25, 30]
    })
