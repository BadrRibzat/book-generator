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
        
        # Map domains to their valid sub-niches (updated to match API)
        domain_niches = {
            'ai_digital_transformation': [
                'ai_business_automation', 'machine_learning_basics', 'digital_transformation_strategy',
                'ai_ethics_governance', 'chatgpt_productivity', 'data_driven_decisions',
                'ai_content_creation', 'automation_workflows'
            ],
            'sustainability_green_tech': [
                'renewable_energy_solutions', 'circular_economy_principles', 'green_technology_innovations',
                'carbon_neutral_living', 'sustainable_supply_chain', 'eco_friendly_investing',
                'green_building_design', 'climate_tech_startups'
            ],
            'mental_health_tech': [
                'ai_mental_health_apps', 'digital_wellness_tools', 'teletherapy_platforms',
                'mental_health_ai_diagnostics', 'stress_management_apps', 'cognitive_behavioral_tech',
                'mental_health_wearables', 'workplace_mental_health_tech'
            ],
            'future_skills': [
                'remote_work_mastery', 'blockchain_cryptocurrency', 'metaverse_virtual_reality',
                'cybersecurity_essentials', 'digital_entrepreneurship', 'quantum_computing_basics',
                'iot_smart_homes', 'nft_digital_assets'
            ],
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
