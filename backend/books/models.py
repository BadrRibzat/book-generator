from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Domain(models.Model):
    """
    Book domain/category model - admin managed
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon name")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Niche(models.Model):
    """Book niche linked to a domain with generation metadata."""

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='niches')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    prompt_template = models.TextField(
        blank=True,
        default="",
        help_text="Prompt template injected into the LLM for this niche"
    )
    content_skeleton = models.JSONField(
        default=list,
        help_text="Ordered outline the generator must follow for this niche"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['domain', 'order', 'name']
        unique_together = ['domain', 'slug']

    def __str__(self):
        return f"{self.name} ({self.domain.name})"


class CoverStyle(models.Model):
    """
    Cover style options for book covers
    """
    STYLE_CHOICES = [
        ('minimalist', 'Minimalist'),
        ('futuristic', 'Futuristic'),
        ('playful', 'Playful'),
        ('elegant', 'Elegant'),
        ('corporate', 'Corporate'),
        ('artistic', 'Artistic'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES)
    description = models.TextField(blank=True)
    preview_image = models.ImageField(upload_to='cover_styles/', blank=True, null=True)
    color_scheme = models.JSONField(default=dict, help_text="Primary and accent colors")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.style})"


class FontTheme(models.Model):
    """
    Font theme configuration with domain-based defaults and AI brief override
    Integrates with Google Fonts CSS2 API for dynamic font loading
    """
    FONT_CATEGORY_CHOICES = [
        ('clean_sans', 'Clean Sans-Serif'),
        ('elegant_serif', 'Elegant Serif'),
        ('hand_written', 'Hand-Written/Script'),
        ('modern_geometric', 'Modern Geometric'),
        ('classic_traditional', 'Classic Traditional'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=30, choices=FONT_CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    
    # Domain relationship (optional - can be domain-specific or global)
    domain = models.ForeignKey(
        Domain, 
        on_delete=models.SET_NULL, 
        related_name='font_themes',
        blank=True,
        null=True,
        help_text="If set, this font theme is default for this domain"
    )
    
    # Font family names (Google Fonts compatible)
    header_font = models.CharField(
        max_length=100,
        default='Inter',
        help_text="Google Font name for headers (e.g., 'Inter', 'Playfair Display')"
    )
    body_font = models.CharField(
        max_length=100,
        default='Lato',
        help_text="Google Font name for body text (e.g., 'Lato', 'Source Serif Pro')"
    )
    
    # Font weights
    header_weight = models.IntegerField(
        default=700,
        help_text="Font weight for headers (400=normal, 700=bold, 900=black)"
    )
    body_weight = models.IntegerField(
        default=400,
        help_text="Font weight for body text (400=normal, 600=semi-bold)"
    )
    
    # AI brief keywords for auto-selection
    ai_brief_keywords = models.JSONField(
        default=list,
        help_text="Keywords in cover brief that trigger this font theme (e.g., ['modern', 'tech', 'minimal'])"
    )
    
    # Google Fonts CSS2 API URL (auto-generated)
    google_fonts_url = models.TextField(
        blank=True,
        help_text="Auto-generated Google Fonts CSS2 API URL"
    )
    
    # Priority for auto-selection (higher = preferred)
    priority = models.IntegerField(default=50)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(
        default=False,
        help_text="Use as default when no domain or AI match"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'name']
        indexes = [
            models.Index(fields=['domain', 'is_active']),
            models.Index(fields=['category']),
            models.Index(fields=['is_default']),
        ]
    
    def __str__(self):
        domain_str = f" ({self.domain.name})" if self.domain else " (Global)"
        return f"{self.name}{domain_str}"
    
    def save(self, *args, **kwargs):
        """Auto-generate Google Fonts CSS2 API URL"""
        if self.header_font and self.body_font:
            # Build Google Fonts CSS2 API URL
            # Format: https://fonts.googleapis.com/css2?family=Font+Name:wght@weight&family=Font2:wght@weight&display=swap
            header_family = self.header_font.replace(' ', '+')
            body_family = self.body_font.replace(' ', '+')
            
            self.google_fonts_url = (
                f"https://fonts.googleapis.com/css2?"
                f"family={header_family}:wght@{self.header_weight}&"
                f"family={body_family}:wght@{self.body_weight}&"
                f"display=swap"
            )
        
        # Ensure only one default exists
        if self.is_default:
            FontTheme.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        
        super().save(*args, **kwargs)
    
    @classmethod
    def select_font_theme_from_brief(cls, cover_brief: str, domain=None) -> 'FontTheme':
        """
        Select appropriate font theme based on cover brief AI analysis
        
        Args:
            cover_brief: AI-generated cover design brief
            domain: Book domain (optional)
            
        Returns:
            FontTheme: Best matching font theme
        """
        brief_lower = cover_brief.lower()
        
        # Try domain-specific themes first
        if domain:
            domain_themes = cls.objects.filter(domain=domain, is_active=True)
            
            for theme in domain_themes:
                keywords = theme.ai_brief_keywords or []
                if any(keyword.lower() in brief_lower for keyword in keywords):
                    return theme
        
        # Try global themes with keyword matching
        global_themes = cls.objects.filter(domain__isnull=True, is_active=True).order_by('-priority')
        
        for theme in global_themes:
            keywords = theme.ai_brief_keywords or []
            if any(keyword.lower() in brief_lower for keyword in keywords):
                return theme
        
        # Fallback to default
        default = cls.objects.filter(is_default=True, is_active=True).first()
        if default:
            return default
        
        # Ultimate fallback - create or get a basic theme
        basic_theme, created = cls.objects.get_or_create(
            name='Professional Default',
            defaults={
                'category': 'clean_sans',
                'header_font': 'Inter',
                'body_font': 'Lato',
                'header_weight': 700,
                'body_weight': 400,
                'is_default': True,
                'ai_brief_keywords': ['professional', 'clean', 'modern']
            }
        )
        return basic_theme


class Book(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generating', 'Generating Content'),
        ('content_generated', 'Content Generated'),
        ('cover_pending', 'Awaiting Cover Selection'),
        ('ready', 'Ready for Download'),
        ('error', 'Generation Error'),
    ]

    BOOK_LENGTH_CHOICES = [
        ('short', 'Short (~20-25 pages)'),
        ('standard', 'Standard (~35-45 pages)'),
        ('long', 'Long (~50-70 pages)'),
    ]
    
    # Core fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)  # Auto-generated
    
    # New relationships
    domain = models.ForeignKey(Domain, on_delete=models.PROTECT, related_name='books')
    niche = models.ForeignKey(Niche, on_delete=models.PROTECT, related_name='books')
    cover_style = models.ForeignKey(CoverStyle, on_delete=models.PROTECT, related_name='books', blank=True, null=True)
    book_length = models.CharField(
        max_length=15,
        choices=BOOK_LENGTH_CHOICES,
        default='standard',
        help_text="Driving page count and chapter depth"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Progress tracking
    progress_percentage = models.IntegerField(default=0, help_text="Generation progress 0-100")
    current_step = models.CharField(max_length=100, blank=True, help_text="Current generation step")
    
    # MongoDB reference for content
    mongodb_id = models.CharField(max_length=100, blank=True, null=True)
    
    # SaaS Features
    subscription_plan = models.ForeignKey(
        'users.SubscriptionPlan',
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
    
    # Quality tracking
    quality_score = models.IntegerField(
        default=0,
        help_text="Automated content quality score (0-100)"
    )
    
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
            base_cost_per_page = 0.50

            if profile.subscription_tier == 'parents':
                discount = 0.1
            elif profile.subscription_tier == 'creators':
                discount = 0.2
            else:
                discount = 0

            min_pages, max_pages = self.get_page_count_range()
            cost = (max_pages * base_cost_per_page) * (1 - discount)
            self.cost_to_generate = round(cost, 2)
            self.save()

    def get_page_count_range(self):
        """Return (min_pages, max_pages) for the selected book length."""
        return {
            'short': (20, 25),
            'standard': (35, 45),
            'long': (50, 70),
        }.get(self.book_length, (35, 45))
    
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
    domain = models.ForeignKey(Domain, on_delete=models.PROTECT, related_name='templates', default=1)
    niche = models.ForeignKey(Niche, on_delete=models.PROTECT, related_name='templates', default=1)
    
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
