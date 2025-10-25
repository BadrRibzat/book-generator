from rest_framework import serializers
from .models import SubscriptionPlan, Subscription, Payment

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for subscription plans"""
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'plan_type', 'price', 'currency', 'interval',
            'max_books_per_month', 'max_pages_per_book', 'priority_support',
            'custom_covers', 'api_access', 'is_active'
        ]
        read_only_fields = ['id', 'is_active']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for user subscriptions"""
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'plan', 'plan_id', 'status', 'current_period_start',
            'current_period_end', 'cancel_at_period_end', 'is_active',
            'can_generate_books', 'created_at'
        ]
        read_only_fields = [
            'id', 'status', 'current_period_start', 'current_period_end',
            'cancel_at_period_end', 'is_active', 'can_generate_books', 'created_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments"""
    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'payment_type', 'amount', 'currency', 'status',
            'subscription', 'book', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']


class CreateSubscriptionSerializer(serializers.Serializer):
    """Serializer for creating subscriptions"""
    plan_id = serializers.IntegerField()
    payment_method_id = serializers.CharField(required=False)

    def validate_plan_id(self, value):
        try:
            plan = SubscriptionPlan.objects.get(id=value, is_active=True)
            return value
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive subscription plan")


class StripeWebhookSerializer(serializers.Serializer):
    """Serializer for Stripe webhook data"""
    id = serializers.CharField()
    object = serializers.CharField()
    api_version = serializers.CharField()
    created = serializers.IntegerField()
    data = serializers.DictField()
    livemode = serializers.BooleanField()
    pending_webhooks = serializers.IntegerField()
    request = serializers.DictField()
    type = serializers.CharField()