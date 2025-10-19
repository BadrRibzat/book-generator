# books/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book
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
    selected_cover = CoverSerializer(read_only=True)
    can_download = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'user_username', 'title', 'domain', 'sub_niche', 'page_length', 
                  'status', 'created_at', 'updated_at', 'completed_at', 'content_generated_at',
                  'covers', 'selected_cover', 'can_download', 'download_url',
                  'error_message', 'mongodb_id']
        read_only_fields = ['id', 'title', 'status', 'created_at', 
                           'updated_at', 'completed_at', 'content_generated_at', 'error_message', 'mongodb_id']
    
    def get_can_download(self, obj):
        return obj.can_download()
    
    def get_download_url(self, obj):
        if obj.can_download():
            return f"/api/books/{obj.id}/download/"
        return None

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['domain', 'sub_niche', 'page_length']
    
    def validate_sub_niche(self, value):
        """Ensure sub_niche matches the selected domain"""
        domain = self.initial_data.get('domain')
        
        domain_niches = {
            'language_kids': ['ai_learning_stories', 'multilingual_coloring', 'kids_mindful_journals'],
            'tech_ai': ['ai_ethics', 'nocode_guides', 'smart_home_diy'],
            'nutrition': ['specialty_diet', 'plant_based_cooking', 'nutrition_mental_health'],
            'meditation': ['mindfulness_anxiety', 'sleep_meditation', 'gratitude_journals'],
            'home_workout': ['equipment_free', 'yoga_remote_workers', 'mobility_training'],
        }
        
        if value not in domain_niches.get(domain, []):
            raise serializers.ValidationError(
                f"Sub-niche '{value}' not valid for domain '{domain}'"
            )
        
        return value
    
    def create(self, validated_data):
        # Import here to avoid circular imports
        from books.services.book_generator import BookGenerator
        
        # Auto-generate title
        generator = BookGenerator()
        title = generator.generate_title(validated_data['sub_niche'])
        
        # Create book with auto-generated title
        book = Book.objects.create(
            user=self.context['request'].user,
            title=title,
            **validated_data
        )
        
        return book
