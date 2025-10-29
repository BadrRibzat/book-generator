# books/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Book, BookTemplate, Domain, Niche, CoverStyle
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
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'prompt_template',
            'content_skeleton',
            'domain',
            'domain_name',
            'domain_slug',
            'is_active',
            'order',
        ]


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
    # Return slugs for domain and niche for frontend compatibility
    domain = serializers.CharField(source='domain.slug', read_only=True)
    niche = serializers.CharField(source='niche.slug', read_only=True)
    domain_name = serializers.CharField(source='domain.name', read_only=True)
    niche_name = serializers.CharField(source='niche.name', read_only=True)
    cover_style_name = serializers.CharField(source='cover_style.name', read_only=True, allow_null=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    page_length = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'user_username', 'title', 'domain', 'domain_name', 'niche', 'niche_name', 
                  'book_length', 'cover_style', 'cover_style_name',
                  'status', 'created_at', 'updated_at', 'completed_at', 'content_generated_at',
                  'covers', 'selected_cover', 'can_download', 'download_url', 'page_length', 'quality_score',
                  'error_message', 'mongodb_id', 'progress_percentage', 'current_step']
        read_only_fields = ['id', 'title', 'status', 'created_at', 
                           'updated_at', 'completed_at', 'content_generated_at', 'error_message', 'mongodb_id']
    
    def get_page_length(self, obj):
        """Expose the upper bound of the selected page range."""
        return obj.get_page_count_range()[1]
    
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
    domain = serializers.CharField()
    niche = serializers.CharField()
    cover_style = serializers.CharField(required=False, allow_blank=True)
    book_length = serializers.ChoiceField(
        choices=[choice for choice in Book.BOOK_LENGTH_CHOICES],
        default='standard'
    )
    
    class Meta:
        model = Book
        fields = ['domain', 'niche', 'cover_style', 'book_length']
    
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
    
    def validate(self, attrs):
        domain = attrs.get('domain')
        niche = attrs.get('niche')

        if domain and niche and niche.domain_id != domain.id:
            raise serializers.ValidationError({
                'niche': f"Selected niche '{niche.name}' does not belong to domain '{domain.name}'."
            })

        return attrs

    def create(self, validated_data):
        from backend.utils.mongodb import get_mongodb_db

        book_fields = ['domain', 'niche', 'cover_style', 'book_length']
        book_data = {field: validated_data[field] for field in book_fields if field in validated_data}

        book = Book.objects.create(
            user=self.context['request'].user,
            title="Generating...",
            **book_data
        )

        niche = book.niche
        generation_params = {
            'book_id': book.id,
            'book_length': validated_data.get('book_length', 'standard'),
            'domain_slug': book.domain.slug,
            'niche_slug': niche.slug if niche else None,
            'prompt_template': niche.prompt_template if niche else '',
            'content_skeleton': niche.content_skeleton if niche else [],
            'created_at': timezone.now().isoformat()
        }

        try:
            db = get_mongodb_db()
            params_collection = db['book_generation_params']
            params_collection.insert_one(generation_params)
            print(f"Stored generation parameters in MongoDB for book {book.id}: {generation_params}")
        except Exception as e:
            print(f"Failed to store generation parameters in MongoDB: {e}")

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
