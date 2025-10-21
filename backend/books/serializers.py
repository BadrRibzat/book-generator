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
            'personal_development': ['productivity_home', 'self_esteem', 'parenting_guidance', 'mental_health'],
            'business_entrepreneurship': ['online_business', 'investing_basics', 'marketing_guide', 'business_planning'],
            'health_wellness': ['general_health', 'autoimmune_living', 'holistic_wellness', 'fitness_nutrition'],
            'relationships': ['dating_advice', 'marriage_tips', 'conflict_resolution', 'communication_skills'],
            'childrens_books': ['early_readers', 'religion_manners', 'educational_fun', 'bedtime_stories'],
            'education_learning': ['study_techniques', 'exam_preparation', 'language_learning', 'online_learning'],
            'technology_digital': ['coding_basics', 'graphic_design', 'social_media_marketing', 'digital_tools'],
            'finance_investment': ['personal_finance', 'investment_strategies', 'retirement_planning', 'financial_independence'],
            'hobbies_interests': ['cooking_recipes', 'diy_crafts', 'gardening_guide', 'photography_tips'],
            'travel_adventure': ['travel_guides', 'budget_travel', 'adventure_planning', 'cultural_exploration'],
            'productivity_time': ['time_management', 'organization_tips', 'goal_setting', 'workflow_optimization'],
            'creative_writing': ['writing_techniques', 'creative_prompts', 'genre_writing', 'publishing_guide'],
            'sustainability_eco': ['zero_waste', 'renewable_energy', 'sustainable_products', 'eco_living'],
            'ai_future_tech': ['ai_concepts', 'ai_ethics', 'future_tech_trends', 'automation_impact'],
            'mindfulness_meditation': ['mindfulness_practices', 'meditation_techniques', 'stress_reduction', 'inner_peace'],
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
