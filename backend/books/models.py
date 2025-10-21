from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import UserProfile, SubscriptionPlan


class Book(models.Model):
    """
    Enhanced Book model with SaaS features and usage tracking
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generating', 'Generating Content'),
        ('content_generated', 'Content Generated'),
        ('cover_pending', 'Awaiting Cover Selection'),
        ('ready', 'Ready for Download'),
        ('error', 'Generation Error'),
    ]
    
    DOMAIN_CHOICES = [
        ('personal_development', 'Personal Development'),
        ('business_entrepreneurship', 'Business & Entrepreneurship'),
        ('health_wellness', 'Health & Wellness'),
        ('relationships', 'Relationships'),
        ('childrens_books', "Children's Books"),
        ('education', 'Education'),
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('hobbies', 'Hobbies'),
        ('travel', 'Travel'),
        ('productivity', 'Productivity'),
        ('creative_writing', 'Creative Writing'),
        ('sustainability', 'Sustainability'),
        ('ai_future_tech', 'AI & Future Tech'),
        ('mindfulness', 'Mindfulness'),
    ]
    
    SUB_NICHE_CHOICES = [
        # Personal Development
        ('productivity_home', 'Boosting Productivity When Working From Home'),
        ('self_esteem', 'Building Self-Esteem and Confidence'),
        ('parenting_guidance', 'Modern Parenting Guidance'),
        ('mental_health', 'Mental Health and Mindset'),
        
        # Business & Entrepreneurship
        ('online_business', 'Starting an Online Business'),
        ('investing_basics', 'Investment Strategies for Beginners'),
        ('marketing_guide', 'Digital Marketing Step-by-Step'),
        ('business_planning', 'Business Planning Tools and Resources'),
        
        # Health & Wellness
        ('general_health', 'General Health and Nutrition'),
        ('autoimmune_living', 'Living with Autoimmune Diseases'),
        ('holistic_wellness', 'Holistic Wellness Approaches'),
        ('fitness_nutrition', 'Fitness and Nutrition Basics'),
        
        # Relationships
        ('dating_advice', 'Modern Dating Advice'),
        ('marriage_tips', 'Marriage and Partnership Tips'),
        ('conflict_resolution', 'Handling Relationship Conflicts'),
        ('communication_skills', 'Effective Communication Skills'),
        
        # Children's Books
        ('early_readers', 'Short Stories for Early Readers'),
        ('religion_manners', 'Religion and Good Manners'),
        ('educational_fun', 'Fun Educational Activities'),
        ('bedtime_stories', 'Bedtime Stories and Morals'),
        
        # Education & Learning
        ('study_techniques', 'Study Techniques and Methods'),
        ('exam_preparation', 'Exam Preparation Strategies'),
        ('language_learning', 'Language Learning Guides'),
        ('online_learning', 'Online Learning Best Practices'),
        
        # Technology & Digital Skills
        ('coding_basics', 'Coding for Beginners'),
        ('graphic_design', 'Graphic Design Fundamentals'),
        ('social_media_marketing', 'Social Media Marketing'),
        ('digital_tools', 'Digital Tools and Productivity'),
        
        # Finance & Investment
        ('personal_finance', 'Personal Finance Management'),
        ('investment_strategies', 'Investment Strategies'),
        ('retirement_planning', 'Retirement Planning Guide'),
        ('financial_independence', 'Path to Financial Independence'),
        
        # Hobbies & Interests
        ('cooking_recipes', 'Cooking and Recipe Collections'),
        ('diy_crafts', 'DIY Crafts and Projects'),
        ('gardening_guide', 'Gardening for Beginners'),
        ('photography_tips', 'Photography Tips and Techniques'),
        
        # Travel & Adventure
        ('travel_guides', 'Destination Travel Guides'),
        ('budget_travel', 'Budget Travel Tips'),
        ('adventure_planning', 'Adventure and Trip Planning'),
        ('cultural_exploration', 'Cultural Exploration Guides'),
        
        # Productivity & Time Management
        ('time_management', 'Effective Time Management'),
        ('organization_tips', 'Organization and Decluttering'),
        ('goal_setting_achievement', 'Goal Setting and Achievement'),
        ('workflow_optimization', 'Workflow Optimization'),
        
        # Creative Writing & Storytelling
        ('writing_techniques', 'Writing Techniques and Style'),
        ('creative_prompts', 'Creative Writing Prompts'),
        ('genre_writing', 'Genre-Specific Writing Advice'),
        ('publishing_guide', 'Publishing and Marketing for Authors'),
        
        # Sustainability & Eco-Friendly Living
        ('zero_waste', 'Zero Waste Lifestyle'),
        ('renewable_energy', 'Renewable Energy for Homes'),
        ('sustainable_products', 'Sustainable Product Choices'),
        ('eco_living', 'Eco-Friendly Living Tips'),
        
        # AI & Future Technologies
        ('ai_concepts', 'Understanding AI Concepts'),
        ('ai_ethics', 'AI Ethics and Considerations'),
        ('future_tech_trends', 'Future Technology Trends'),
        ('automation_impact', 'Automation and Its Impact'),
        
        # Mindfulness & Meditation
        ('mindfulness_practices', 'Daily Mindfulness Practices'),
        ('meditation_techniques', 'Meditation Techniques for Beginners'),
        ('stress_reduction', 'Stress Reduction Methods'),
        ('inner_peace', 'Finding Inner Peace and Balance'),
    ]
    
    PAGE_LENGTH_CHOICES = [
        (15, '15 Pages'),
        (20, '20 Pages'),
        (25, '25 Pages'),
        (30, '30 Pages'),
    ]
    
    # Core fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)  # Auto-generated
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    sub_niche = models.CharField(max_length=50, choices=SUB_NICHE_CHOICES)
    page_length = models.IntegerField(choices=PAGE_LENGTH_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # MongoDB reference for content
    mongodb_id = models.CharField(max_length=100, blank=True, null=True)
    
    # SaaS Features
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='books'
    )
    
    # Revenue tracking
    cost_to_generate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Cost to generate this book"
    )
    currency = models.CharField(
        max_length=3, 
        default='USD',
        help_text="Currency for this book"
    )
    
    # Usage tracking
    generation_time_seconds = models.IntegerField(default=0)
    generation_started_at = models.DateTimeField(blank=True, null=True)
    generation_completed_at = models.DateTimeField(blank=True, null=True)
    
    # Commercial usage
    is_commercial = models.BooleanField(default=False)
    commercial_license_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ('personal', 'Personal Use Only'),
            ('commercial', 'Commercial Use'),
            ('resell', 'Resell Rights'),
        ]
    )
    
    # Sharing and collaboration
    is_shared = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_books')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_generated_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Error tracking
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['domain']),
            models.Index(fields=['subscription_plan']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"
    
    def can_download(self):
        """Check if book is ready for download"""
        return self.status == 'ready' and self.selected_cover is not None
    
    @property
    def selected_cover(self):
        """Get the selected cover for this book"""
        return self.covers.filter(is_selected=True).first()
    
    @property
    def total_cost(self):
        """Calculate total cost including generation and downloads"""
        downloads_cost = self.downloads.count() * 0  # Add download costs if applicable
        return self.cost_to_generate + downloads_cost
    
    @property
    def is_free_tier(self):
        """Check if this book was created by a free tier user"""
        if hasattr(self.user, 'profile'):
            return self.user.profile.subscription_tier == 'free'
        return False
    
    @property
    def is_within_limits(self):
        """Check if book creation was within user's subscription limits"""
        if hasattr(self.user, 'profile'):
            profile = self.user.profile
            return profile.can_create_book()
        return False
    
    def track_generation_start(self):
        """Mark when generation started"""
        self.generation_started_at = timezone.now()
        self.save()
    
    def track_generation_complete(self):
        """Mark when generation completed and calculate duration"""
        self.generation_completed_at = timezone.now()
        if self.generation_started_at:
            duration = self.generation_completed_at - self.generation_started_at
            self.generation_time_seconds = int(duration.total_seconds())
        self.save()
    
    def calculate_generation_cost(self):
        """Calculate cost based on page length and subscription tier"""
        if hasattr(self.user, 'profile'):
            profile = self.user.profile
            base_cost_per_page = 0.50  # Base cost per page
            
            # Apply subscription discounts
            if profile.subscription_tier == 'basic':
                discount = 0.1  # 10% discount
            elif profile.subscription_tier == 'premium':
                discount = 0.2  # 20% discount
            elif profile.subscription_tier == 'enterprise':
                discount = 0.3  # 30% discount
            else:
                discount = 0  # No discount for free tier
            
            cost = (self.page_length * base_cost_per_page) * (1 - discount)
            self.cost_to_generate = round(cost, 2)
            self.save()
    
    def record_download(self, request):
        """Record a download with analytics"""
        from users.models import DownloadHistory
        
        download = DownloadHistory.objects.create(
            user=self.user,
            book=self,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )
        
        # Update user's download count
        if hasattr(self.user, 'profile'):
            self.user.profile.increment_book_usage()
        
        return download
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def generate_referral_link(self):
        """Generate referral link for this book"""
        if hasattr(self.user, 'profile') and self.user.profile.referral_code:
            # This would need request context to build absolute URI
            # For now, return relative URL
            book_url = f"/books/{self.pk}/"
            referral_url = f"{book_url}?ref={self.user.profile.referral_code}"
            return referral_url
        return None


class BookTemplate(models.Model):
    """
    Custom templates for advanced users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    domain = models.CharField(max_length=50, choices=Book.DOMAIN_CHOICES)
    sub_niche = models.CharField(max_length=50, choices=Book.SUB_NICHE_CHOICES)
    
    # Template content
    title_template = models.CharField(max_length=200, help_text="Template for generating title")
    outline = models.TextField(help_text="Template book outline")
    style_guide = models.TextField(blank=True, null=True, help_text="Writing style guidelines")
    
    # Settings
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['domain']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save()
