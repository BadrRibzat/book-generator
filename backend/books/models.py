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
        ('ai_digital_transformation', 'AI & Digital Transformation'),
        ('sustainability_green_tech', 'Sustainability & Green Tech'),
        ('mental_health_tech', 'Mental Health Technology'),
        ('future_skills', 'Future Skills & Digital Economy'),
    ]
    
    SUB_NICHE_CHOICES = [
        # AI & Digital Transformation
        ('ai_business_automation', 'AI-Powered Business Automation'),
        ('machine_learning_basics', 'Machine Learning for Non-Technical Professionals'),
        ('digital_transformation_strategy', 'Digital Transformation Strategy'),
        ('ai_ethics_governance', 'AI Ethics and Responsible AI Governance'),
        ('chatgpt_productivity', 'ChatGPT and AI Tools for Productivity'),
        ('data_driven_decisions', 'Data-Driven Decision Making'),
        ('ai_content_creation', 'AI-Powered Content Creation'),
        ('automation_workflows', 'Building Automation Workflows'),
        
        # Sustainability & Green Tech
        ('renewable_energy_solutions', 'Renewable Energy Solutions for Homes'),
        ('circular_economy_principles', 'Circular Economy and Sustainable Business'),
        ('green_technology_innovations', 'Green Technology Innovations'),
        ('carbon_neutral_living', 'Carbon Neutral Living Guide'),
        ('sustainable_supply_chain', 'Building Sustainable Supply Chains'),
        ('eco_friendly_investing', 'Eco-Friendly Investing Strategies'),
        ('green_building_design', 'Green Building and Architecture'),
        ('climate_tech_startups', 'Climate Tech Startups and Innovation'),
        
        # Mental Health Technology
        ('ai_mental_health_apps', 'AI-Powered Mental Health Applications'),
        ('digital_wellness_tools', 'Digital Wellness and Mindfulness Tech'),
        ('teletherapy_platforms', 'Teletherapy and Online Counseling'),
        ('mental_health_ai_diagnostics', 'AI Diagnostics for Mental Health'),
        ('stress_management_apps', 'Stress Management Mobile Applications'),
        ('cognitive_behavioral_tech', 'Technology in Cognitive Behavioral Therapy'),
        ('mental_health_wearables', 'Mental Health Wearables and Biofeedback'),
        ('workplace_mental_health_tech', 'Workplace Mental Health Technology Solutions'),
        
        # Future Skills & Digital Economy
        ('remote_work_mastery', 'Remote Work Mastery and Digital Nomad Skills'),
        ('blockchain_cryptocurrency', 'Blockchain and Cryptocurrency Fundamentals'),
        ('metaverse_virtual_reality', 'Metaverse and Virtual Reality Skills'),
        ('cybersecurity_essentials', 'Cybersecurity Essentials for Everyone'),
        ('digital_entrepreneurship', 'Digital Entrepreneurship in the 2020s'),
        ('quantum_computing_basics', 'Quantum Computing for Business Leaders'),
        ('iot_smart_homes', 'IoT and Smart Home Technology'),
        ('nft_digital_assets', 'NFTs and Digital Asset Management'),
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
