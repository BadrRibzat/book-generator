from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import User
import uuid

class SubscriptionPlan(models.Model):
    """Subscription plans for the SaaS platform"""
    PLAN_TYPES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    stripe_price_id = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price in USD
    currency = models.CharField(max_length=3, default='usd')
    interval = models.CharField(max_length=20, choices=[('month', 'Monthly'), ('year', 'Yearly')])

    # Feature limits
    max_books_per_month = models.IntegerField(default=0)  # 0 = unlimited for enterprise
    max_pages_per_book = models.IntegerField(default=30)
    priority_support = models.BooleanField(default=False)
    custom_covers = models.BooleanField(default=False)
    api_access = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (${self.price}/{self.interval})"

    class Meta:
        ordering = ['price']


class Subscription(models.Model):
    """User subscriptions"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('incomplete', 'Incomplete'),
        ('incomplete_expired', 'Incomplete Expired'),
        ('trialing', 'Trialing'),
        ('unpaid', 'Unpaid'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    stripe_subscription_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')
    current_period_start = models.DateTimeField(blank=True, null=True)
    current_period_end = models.DateTimeField(blank=True, null=True)
    cancel_at_period_end = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def can_generate_books(self):
        """Check if user can generate more books this month"""
        if self.plan.max_books_per_month == 0:  # Unlimited
            return True

        from books.models import Book  # Import here to avoid circular import
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        books_this_month = Book.objects.filter(
            user=self.user,
            created_at__gte=current_month
        ).count()

        return books_this_month < self.plan.max_books_per_month


class Payment(models.Model):
    """Payment records"""
    PAYMENT_TYPES = [
        ('subscription', 'Subscription'),
        ('one_time', 'One-time Purchase'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)

    stripe_payment_intent_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=100, blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # For subscription payments
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)

    # For one-time purchases (future use)
    book = models.ForeignKey('books.Book', on_delete=models.SET_NULL, blank=True, null=True)

    metadata = models.JSONField(blank=True, null=True)  # Store additional Stripe data

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.status})"


class WebhookEvent(models.Model):
    """Store Stripe webhook events to prevent duplicate processing"""
    stripe_event_id = models.CharField(max_length=100, unique=True)
    event_type = models.CharField(max_length=100)
    data = models.JSONField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.stripe_event_id}"
