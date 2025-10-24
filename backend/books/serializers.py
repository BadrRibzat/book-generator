# books/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, BookTemplate, Domain, Niche, BookStyle, CoverStyle
from covers.models import Cover

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active', 'order']


class NicheSerializer(serializers.ModelSerializer):
    domain = serializers.PrimaryKeyRelatedField(read_only=True)
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    domain_slug = serializers.CharField(source='domain.slug', read_only=True)
    
    class Meta:
        model = Niche
        fields = ['id', 'name', 'slug', 'description', 'audience', 'market_size', 'domain', 'domain_name', 'domain_slug', 'is_active', 'order']


class BookStyleSerializer(serializers.ModelSerializer):
    page_count_range = serializers.SerializerMethodField()
    
    class Meta:
        model = BookStyle
        fields = ['id', 'name', 'tone', 'target_audience', 'language', 'length', 'description', 'is_active', 'order', 'page_count_range']
    
    def get_page_count_range(self, obj):
        return obj.page_count_range


class CoverStyleSerializer(serializers.ModelSerializer):
    preview_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CoverStyle
        fields = ['id', 'name', 'style', 'description', 'preview_image', 'preview_image_url', 'color_scheme', 'is_active', 'order']
    
    def get_preview_image_url(self, obj):
        if obj.preview_image:
            from django.conf import settings
            return f"{settings.MEDIA_URL}{obj.preview_image}"
        return None


class CoverSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Cover
        fields = ['id', 'template_style', 'image_path', 'image_url', 
                  'is_selected', 'created_at', 'generation_params']
        read_only_fields = ['id', 'created_at']
    
    def get_image_url(self, obj):
        from django.conf import settings
        return f"{settings.MEDIA_URL}{obj.image_path}"


class BookSerializer(serializers.ModelSerializer):
    covers = CoverSerializer(many=True, read_only=True)
    selected_cover = serializers.SerializerMethodField()
    can_download = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    niche_name = serializers.CharField(source='niche.name', read_only=True)
    book_style_name = serializers.CharField(source='book_style.name', read_only=True)
    cover_style_name = serializers.CharField(source='cover_style.name', read_only=True, allow_null=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    page_length = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'user_username', 'title', 'domain', 'domain_name', 'niche', 'niche_name', 
                  'book_style', 'book_style_name', 'cover_style', 'cover_style_name',
                  'status', 'created_at', 'updated_at', 'completed_at', 'content_generated_at',
                  'covers', 'selected_cover', 'can_download', 'download_url', 'page_length',
                  'error_message', 'mongodb_id', 'progress_percentage', 'current_step']
        read_only_fields = ['id', 'title', 'status', 'created_at', 
                           'updated_at', 'completed_at', 'content_generated_at', 'error_message', 'mongodb_id']
    
    def get_page_length(self, obj):
        """Get page length from book style"""
        if obj.book_style:
            return obj.book_style.page_count_range[1]  # Return max pages
        return 20  # Default fallback
    
    def get_selected_cover(self, obj):
        """Get selected cover data, return None if no cover selected"""
        selected_cover = obj.selected_cover
        if selected_cover:
            return CoverSerializer(selected_cover).data
        return None
    
    def get_can_download(self, obj):
        """Check if book can be downloaded"""
        return obj.can_download()
    
    def get_download_url(self, obj):
        """Get download URL if book is ready"""
        if obj.can_download():
            return f"/api/books/{obj.id}/download/"
        return None


class BookCreateSerializer(serializers.ModelSerializer):
    domain = serializers.CharField()  # Accept domain slug as string
    niche = serializers.CharField()   # Accept niche slug as string
    book_style = serializers.CharField()  # Accept book style name/id as string
    cover_style = serializers.CharField(required=False, allow_blank=True)  # Accept cover style name/id as string
    
    # Additional fields from guided workflow (stored for generation)
    book_length = serializers.CharField(required=False, allow_blank=True)
    target_audience = serializers.CharField(required=False, allow_blank=True)
    key_topics = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
    writing_preferences = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Book
        fields = ['domain', 'niche', 'book_style', 'cover_style', 'book_length', 'target_audience', 'key_topics', 'writing_preferences']
    
    def validate_domain(self, value):
        """Convert domain slug to domain object"""
        try:
            return Domain.objects.get(slug=value, is_active=True)
        except Domain.DoesNotExist:
            raise serializers.ValidationError(f"Domain with slug '{value}' not found.")
    
    def validate_niche(self, value):
        """Convert niche ID or slug to niche object"""
        try:
            # Try by ID first
            return Niche.objects.get(id=int(value), is_active=True)
        except (ValueError, Niche.DoesNotExist):
            # Try by slug
            try:
                return Niche.objects.get(slug=value, is_active=True)
            except Niche.DoesNotExist:
                raise serializers.ValidationError(f"Niche '{value}' not found.")
    
    def validate_book_style(self, value):
        """Convert book style ID or name to book style object"""
        try:
            # Try by ID first
            return BookStyle.objects.get(id=int(value), is_active=True)
        except (ValueError, BookStyle.DoesNotExist):
            # Try by name
            try:
                return BookStyle.objects.get(name=value, is_active=True)
            except BookStyle.DoesNotExist:
                raise serializers.ValidationError(f"Book style '{value}' not found.")
    
    def validate_cover_style(self, value):
        """Convert cover style name/id to cover style object"""
        if not value or value == "":
            return None
        try:
            # Try by ID first
            return CoverStyle.objects.get(id=int(value), is_active=True)
        except (ValueError, CoverStyle.DoesNotExist):
            # Try by name
            try:
                return CoverStyle.objects.get(name=value, is_active=True)
            except CoverStyle.DoesNotExist:
                raise serializers.ValidationError(f"Cover style '{value}' not found.")
    
    def create(self, validated_data):
        # Import here to avoid circular imports
        from books.services.book_generator import BookGeneratorProfessional
        
        # Extract fields that belong to the Book model
        book_fields = ['domain', 'niche', 'book_style', 'cover_style']
        book_data = {field: validated_data[field] for field in book_fields if field in validated_data}
        
        # Create book with only the valid Book model fields
        book = Book.objects.create(
            user=self.context['request'].user,
            title="Generating...",  # Placeholder, will be updated during generation
            **book_data
        )
        
        # Store additional generation parameters in MongoDB or pass to generation service
        # These fields are used during content generation but not stored in the Book model
        generation_params = {
            'book_length': validated_data.get('book_length'),
            'target_audience': validated_data.get('target_audience'),
            'key_topics': validated_data.get('key_topics', []),
            'writing_preferences': validated_data.get('writing_preferences')
        }
        
        # You can store these in MongoDB or pass them to the generation service
        # For now, we'll just print them for debugging
        print(f"Book generation parameters: {generation_params}")
        
        return book


class BookStatusSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'status', 'progress_percentage', 'error_message', 'created_at', 'updated_at']
    
    def get_progress_percentage(self, obj):
        status_progress = {
            'draft': 0,
            'generating': 25,
            'content_generated': 50,
            'cover_pending': 75,
            'ready': 100,
            'error': 0,
        }
        return status_progress.get(obj.status, 0)
