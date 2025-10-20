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
        ('self_improvement', 'Self-Improvement & Motivation'),
        ('goal_setting', 'Goal Setting & Achievement'),
        ('confidence_building', 'Confidence Building'),
        
        # Business & Entrepreneurship
        ('startup_guide', 'Startup Guides'),
        ('marketing_basics', 'Marketing Basics'),
        ('leadership_skills', 'Leadership Skills'),
        
        # Health & Wellness
        ('mental_health', 'Mental Health & Wellbeing'),
        ('fitness_nutrition', 'Fitness & Nutrition'),
        ('healthy_habits', 'Healthy Habits'),
        
        # Relationships
        ('communication', 'Communication Skills'),
        ('dating_advice', 'Dating & Relationships'),
        ('family_dynamics', 'Family Dynamics'),
        
        # Children's Books
        ('educational_stories', 'Educational Stories'),
        ('bedtime_stories', 'Bedtime Stories'),
        ('activity_books', 'Activity Books'),
        
        # Education
        ('study_skills', 'Study Skills & Techniques'),
        ('career_guidance', 'Career Guidance'),
        ('skill_development', 'Skill Development'),
        
        # Technology
        ('coding_basics', 'Coding Basics'),
        ('digital_literacy', 'Digital Literacy'),
        ('tech_trends', 'Technology Trends'),
        
        # Finance
        ('personal_finance', 'Personal Finance'),
        ('investing_basics', 'Investing Basics'),
        ('budgeting', 'Budgeting & Saving'),
        
        # Hobbies
        ('arts_crafts', 'Arts & Crafts'),
        ('gardening', 'Gardening'),
        ('cooking', 'Cooking & Recipes'),
        
        # Travel
        ('travel_guides', 'Travel Guides'),
        ('cultural_exploration', 'Cultural Exploration'),
        ('budget_travel', 'Budget Travel'),
        
        # Productivity
        ('time_management', 'Time Management'),
        ('organization', 'Organization Systems'),
        ('workflow_optimization', 'Workflow Optimization'),
        
        # Creative Writing
        ('storytelling', 'Storytelling Techniques'),
        ('poetry', 'Poetry & Verse'),
        ('creative_exercises', 'Creative Writing Exercises'),
        
        # Sustainability
        ('eco_living', 'Eco-Friendly Living'),
        ('renewable_energy', 'Renewable Energy'),
        ('sustainable_practices', 'Sustainable Practices'),
        
        # AI & Future Tech
        ('ai_basics', 'AI Fundamentals'),
        ('future_tech', 'Future Technology'),
        ('digital_transformation', 'Digital Transformation'),
        
        # Mindfulness
        ('meditation_basics', 'Meditation Basics'),
        ('stress_reduction', 'Stress Reduction'),
        ('mindful_living', 'Mindful Living'),
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
            from django.urls import reverse
            book_url = reverse('books:detail', kwargs={'pk': self.pk})
            referral_url = f"{request.build_absolute_uri(book_url)}?ref={self.user.profile.referral_code}"
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
