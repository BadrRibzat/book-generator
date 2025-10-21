from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import uuid


class UserProfile(models.Model):
    """
    Enhanced user profile with subscription and billing information
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    CURRENCY_CHOICES = [
        ('MAD', 'Moroccan Dirham'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile Information
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Demographics (for analytics and localization)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    language = models.CharField(max_length=10, default='en')
    
    # Subscription Information
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('basic', 'Basic - $15/month - 1 book/day'),
            ('premium', 'Premium - $45/month - 3 books/day'),
            ('enterprise', 'Enterprise - $60/month - 5 books/day'),
        ],
        default='free'
    )
    
    subscription_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('cancelled', 'Cancelled'),
            ('expired', 'Expired'),
            ('trial', 'Trial'),
        ],
        default='inactive'
    )
    
    # Billing Information
    billing_email = models.EmailField(blank=True, null=True)
    billing_name = models.CharField(max_length=200, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_country = models.CharField(max_length=100, blank=True, null=True)
    billing_postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Subscription Details
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Usage Limits
    books_per_day = models.IntegerField(default=1)
    books_used_today = models.IntegerField(default=0)
    daily_reset_date = models.DateField(default=timezone.now)
    
    # Referral Information
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    referral_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subscription_tier}"
    
    def can_create_book(self):
        """Check if user can create a new book based on their limits"""
        if self.subscription_tier == 'free':
            return self.books_used_today < 1
        elif self.subscription_tier == 'basic':
            return self.books_used_today < 1
        elif self.subscription_tier == 'premium':
            return self.books_used_today < 3
        elif self.subscription_tier == 'enterprise':
            return self.books_used_today < 5
        return False
    
    def increment_book_usage(self):
        """Increment the daily book usage"""
        self.books_used_today += 1
        self.save()
    
    def reset_daily_usage(self):
        """Reset daily usage at the start of new day"""
        import datetime
        today = timezone.now().date()
        
        # Check if we need to reset (new day)
        if self.daily_reset_date != today:
            self.books_used_today = 0
            self.daily_reset_date = today
            self.save()


class SubscriptionPlan(models.Model):
    """
    Subscription plan definitions
    """
    name = models.CharField(max_length=50)
    tier = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_annual = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Limits
    max_books_per_month = models.IntegerField()
    max_pages_per_book = models.IntegerField(default=30)
    priority_generation = models.BooleanField(default=False)
    commercial_license = models.BooleanField(default=False)
    
    # Features
    ai_enhancement = models.BooleanField(default=True)
    custom_templates = models.BooleanField(default=False)
    team_collaboration = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    
    # Display
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.tier})"
    
    @property
    def monthly_price_display(self):
        return f"{self.currency} {self.price_monthly}"
    
    @property
    def annual_price_display(self):
        return f"{self.currency} {self.price_annual}"
    
    @property
    def discount_percentage(self):
        """Calculate discount for annual plan"""
        if self.price_annual and self.price_monthly:
            annual_equiv = self.price_monthly * 12
            discount = ((annual_equiv - self.price_annual) / annual_equiv) * 100
            return round(discount)
        return 0


class UserActivity(models.Model):
    """
    Track user activity for analytics
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('book_create', 'Create Book'),
        ('book_download', 'Download Book'),
        ('subscription_upgrade', 'Upgrade Subscription'),
        ('subscription_cancel', 'Cancel Subscription'),
        ('profile_update', 'Update Profile'),
        ('payment', 'Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"


class DownloadHistory(models.Model):
    """
    Track book downloads for analytics and billing
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads')
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE, related_name='downloads')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Revenue tracking
    revenue_generated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['book']),
        ]
    
    def __str__(self):
        return f"{self.user.username} downloaded {self.book.title} - {self.timestamp}"


class Payment(models.Model):
    """
    Track all payments for financial records
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_TYPES = [
        ('subscription', 'Subscription'),
        ('one_time', 'One-time Payment'),
        ('upgrade', 'Upgrade'),
        ('refund', 'Refund'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Amount and currency
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Stripe information
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Subscription reference
    subscription = models.ForeignKey('users.Subscription', on_delete=models.SET_NULL, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    failed_at = models.DateTimeField(blank=True, null=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.payment_type} - {self.amount} {self.currency} - {self.status}"


class Subscription(models.Model):
    """
    User subscription management
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('past_due', 'Past Due'),
        ('trial', 'Trial'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    
    # Dates
    started_at = models.DateTimeField(auto_now_add=True)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancelled_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    
    # Stripe information
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_status = models.CharField(max_length=50, blank=True, null=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', '-started_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status}"
    
    def is_active(self):
        """Check if subscription is currently active"""
        return self.status == 'active' and self.current_period_end > timezone.now()
    
    def is_trial(self):
        """Check if subscription is in trial period"""
        return self.status == 'trial' and self.current_period_end > timezone.now()


class Referral(models.Model):
    """
    Track referrals and rewards
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ]
    
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_made')
    referee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals_received')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Reward information
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reward_currency = models.CharField(max_length=3, default='USD')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['referrer', '-created_at']),
            models.Index(fields=['referee']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.referrer.username} referred {self.referee.username} - {self.status}"
