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
        """Validate sub-niche using trending taxonomy"""
        from books.services.trending import TRENDING_NICHES_2025_2027
        
        # Map taxonomy domain names to API keys
        DOMAIN_KEY_MAP = {
            'AI & Digital Transformation': 'ai_digital_transformation',
            'Sustainability & Green Tech': 'sustainability_green_tech',
            'Mental Health Technology': 'mental_health_tech',
            'Future Skills & Digital Economy': 'future_skills'
        }
        
        # Get domain from initial_data
        domain = self.initial_data.get('domain')
        if not domain:
            raise serializers.ValidationError("Domain is required to validate sub-niche")
        
        # Find matching domain in taxonomy
        for domain_name, sub_niches_dict in TRENDING_NICHES_2025_2027.items():
            domain_key = DOMAIN_KEY_MAP.get(domain_name, domain_name.lower().replace(' ', '_').replace('&', '').replace('__', '_').strip('_'))
            
            if domain_key == domain:
                valid_sub_niches = list(sub_niches_dict.keys())
                if value not in valid_sub_niches:
                    raise serializers.ValidationError(
                        f"Invalid sub-niche '{value}' for domain '{domain}'. "
                        f"Valid sub-niches: {', '.join(valid_sub_niches)}"
                    )
                return value
        
        raise serializers.ValidationError(f"Invalid domain: {domain}")
    
    def create(self, validated_data):
        # Import here to avoid circular imports
        from books.services.book_generator import BookGeneratorProfessional
        
        # Create book with placeholder title first
        # The actual title will be extracted during content generation
        book = Book.objects.create(
            user=self.context['request'].user,
            title="Generating...",  # Placeholder, will be updated during generation
            **validated_data
        )
        
        return book
