from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    UserProfile, 
    SubscriptionPlan, 
    UserActivity, 
    DownloadHistory, 
    Payment, 
    Subscription,
    Referral
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Enhanced user profile serializer"""
    user = UserSerializer(read_only=True)
    books_used_this_month = serializers.IntegerField(read_only=True)
    books_per_month = serializers.IntegerField(read_only=True)
    can_create_book = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'user', 'full_name', 'phone', 'avatar', 'bio', 'website',
            'country', 'city', 'currency', 'language',
            'subscription_tier', 'subscription_status',
            'billing_email', 'billing_name', 'billing_address', 'billing_city',
            'billing_country', 'billing_postal_code',
            'books_used_this_month', 'books_per_month', 'can_create_book',
            'referral_code', 'referral_count', 'last_login_ip',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'referral_code', 'referral_count', 'last_login_ip',
            'created_at', 'updated_at'
        ]
    
    def get_can_create_book(self, obj):
        return obj.can_create_book()


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Subscription plan serializer"""
    monthly_price_display = serializers.CharField(read_only=True)
    annual_price_display = serializers.CharField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'tier', 'description', 'price_monthly', 'price_annual',
            'currency', 'max_books_per_month', 'max_pages_per_book',
            'priority_generation', 'commercial_license',
            'ai_enhancement', 'custom_templates', 'team_collaboration', 'priority_support',
            'monthly_price_display', 'annual_price_display', 'discount_percentage',
            'is_active', 'sort_order', 'featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """User activity tracking serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'username', 'activity_type', 'description', 'metadata',
            'ip_address', 'user_agent', 'timestamp'
        ]
        read_only_fields = ['timestamp']


class DownloadHistorySerializer(serializers.ModelSerializer):
    """Download history serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = DownloadHistory
        fields = [
            'id', 'username', 'book', 'book_title', 'timestamp',
            'ip_address', 'user_agent', 'revenue_generated', 'currency'
        ]
        read_only_fields = ['timestamp']


class PaymentSerializer(serializers.ModelSerializer):
    """Payment tracking serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    plan_name = serializers.CharField(source='subscription.plan.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'username', 'payment_type', 'status', 'amount', 'currency',
            'stripe_payment_intent_id', 'stripe_charge_id', 'plan_name',
            'created_at', 'completed_at', 'failed_at', 'metadata', 'notes'
        ]
        read_only_fields = ['created_at', 'completed_at', 'failed_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription management serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_tier = serializers.CharField(source='plan.tier', read_only=True)
    is_active = serializers.SerializerMethodField()
    is_trial = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'username', 'plan', 'plan_name', 'plan_tier', 'status',
            'started_at', 'current_period_start', 'current_period_end',
            'cancelled_at', 'ended_at', 'stripe_subscription_id', 'stripe_status',
            'is_active', 'is_trial', 'metadata', 'notes'
        ]
        read_only_fields = [
            'started_at', 'current_period_start', 'current_period_end',
            'cancelled_at', 'ended_at', 'stripe_subscription_id', 'stripe_status'
        ]
    
    def get_is_active(self, obj):
        return obj.is_active()
    
    def get_is_trial(self, obj):
        return obj.is_trial()


class ReferralSerializer(serializers.ModelSerializer):
    """Referral tracking serializer"""
    referrer_username = serializers.CharField(source='referrer.username', read_only=True)
    referee_username = serializers.CharField(source='referee.username', read_only=True)
    
    class Meta:
        model = Referral
        fields = [
            'id', 'referrer', 'referrer_username', 'referee', 'referee_username',
            'status', 'reward_amount', 'reward_currency',
            'created_at', 'completed_at', 'metadata'
        ]
        read_only_fields = ['created_at', 'completed_at']


class UserAnalyticsSerializer(serializers.Serializer):
    """User analytics data serializer"""
    total_books_created = serializers.IntegerField()
    total_books_downloaded = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_usage = serializers.IntegerField()
    subscription_tier = serializers.CharField()
    account_created_date = serializers.DateTimeField()
    last_activity_date = serializers.DateTimeField()


class SubscriptionCreateSerializer(serializers.Serializer):
    """Subscription creation serializer"""
    plan_tier = serializers.ChoiceField(choices=['basic', 'premium', 'enterprise'])
    billing_email = serializers.EmailField()
    billing_name = serializers.CharField(max_length=200)
    billing_address = serializers.CharField()
    billing_city = serializers.CharField(max_length=100)
    billing_country = serializers.CharField(max_length=100)
    billing_postal_code = serializers.CharField(max_length=20)
    payment_method_id = serializers.CharField()  # Stripe payment method ID
    
    def validate_plan_tier(self, value):
        """Validate that plan exists and is active"""
        try:
            plan = SubscriptionPlan.objects.get(tier=value, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive subscription plan")
        return value


class PaymentIntentSerializer(serializers.Serializer):
    """Create payment intent serializer"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.ChoiceField(choices=['USD', 'EUR', 'MAD'])
    payment_type = serializers.ChoiceField(choices=['subscription', 'one_time'])
    plan_tier = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False)


class ReferralCreateSerializer(serializers.Serializer):
    """Referral creation serializer"""
    referral_code = serializers.CharField(max_length=20)
    
    def validate_referral_code(self, value):
        """Validate referral code exists"""
        try:
            profile = UserProfile.objects.get(referral_code=value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Invalid referral code")
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Update user profile serializer"""
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'phone', 'avatar', 'bio', 'website',
            'country', 'city', 'currency', 'language',
            'billing_email', 'billing_name', 'billing_address', 
            'billing_city', 'billing_country', 'billing_postal_code'
        ]
    
    def update(self, instance, validated_data):
        # Track profile update activity
        UserActivity.objects.create(
            user=instance.user,
            activity_type='profile_update',
            description=f"Updated profile settings",
            metadata=validated_data
        )
        return super().update(instance, validated_data)


class SubscriptionUpgradeSerializer(serializers.Serializer):
    """Subscription upgrade serializer"""
    new_plan_tier = serializers.ChoiceField(choices=['basic', 'premium', 'enterprise'])
    billing_update = serializers.BooleanField(default=False)
    
    def validate_new_plan_tier(self, value):
        """Validate that plan exists and is active"""
        try:
            plan = SubscriptionPlan.objects.get(tier=value, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive subscription plan")
        return value


class UsageReportSerializer(serializers.Serializer):
    """Usage report serializer"""
    period = serializers.ChoiceField(choices=['daily', 'weekly', 'monthly'])
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    
    def validate(self, data):
        """Validate date range"""
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date must be before end date")
        return data
