from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
import logging

from .models import SubscriptionPlan, Subscription, Payment
from .serializers import (
    SubscriptionPlanSerializer, SubscriptionSerializer,
    PaymentSerializer, CreateSubscriptionSerializer
)
from .services import StripeService

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionPlanListView(generics.ListAPIView):
    """List all active subscription plans"""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


class UserSubscriptionView(generics.RetrieveAPIView):
    """Get current user's subscription"""
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Get the user's current/latest subscription"""
        # Return subscription if exists, otherwise return None (frontend handles gracefully)
        try:
            return Subscription.objects.filter(user=self.request.user).latest('created_at')
        except Subscription.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            # Return empty response instead of 404 when no subscription exists
            return Response({
                'status': 'no_subscription',
                'message': 'No active subscription found'
            }, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CreateSubscriptionView(APIView):
    """Create a new subscription for the user"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = SubscriptionPlan.objects.get(id=serializer.validated_data['plan_id'])
            payment_method_id = serializer.validated_data.get('payment_method_id')

            result = StripeService.create_subscription(
                request.user, plan, payment_method_id
            )

            subscription_serializer = SubscriptionSerializer(result['subscription'])

            return Response({
                'subscription': subscription_serializer.data,
                'client_secret': result['client_secret']
            })

        except Exception as e:
            logger.error(f"Failed to create subscription: {str(e)}")
            return Response(
                {'error': 'Failed to create subscription'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CancelSubscriptionView(APIView):
    """Cancel user's subscription"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            subscription = get_object_or_404(Subscription, user=request.user)

            if subscription.status != 'active':
                return Response(
                    {'error': 'Subscription is not active'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            StripeService.cancel_subscription(subscription)

            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Failed to cancel subscription: {str(e)}")
            return Response(
                {'error': 'Failed to cancel subscription'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReactivateSubscriptionView(APIView):
    """Reactivate a canceled subscription"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            subscription = get_object_or_404(Subscription, user=request.user)

            if subscription.status != 'active' or not subscription.cancel_at_period_end:
                return Response(
                    {'error': 'Subscription is not scheduled for cancellation'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            StripeService.reactivate_subscription(subscription)

            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Failed to reactivate subscription: {str(e)}")
            return Response(
                {'error': 'Failed to reactivate subscription'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateSubscriptionView(APIView):
    """Update subscription to a different plan"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        if not plan_id:
            return Response(
                {'error': 'plan_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            subscription = get_object_or_404(Subscription, user=request.user)
            new_plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

            StripeService.update_subscription_plan(subscription, new_plan)

            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Failed to update subscription: {str(e)}")
            return Response(
                {'error': 'Failed to update subscription'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentHistoryView(generics.ListAPIView):
    """Get user's payment history"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    """Handle Stripe webhook events"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )

            # Process the event
            StripeService.handle_webhook_event(event)

            return Response({'status': 'success'})

        except ValueError as e:
            # Invalid payload
            logger.error(f"Invalid webhook payload: {str(e)}")
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            logger.error(f"Invalid webhook signature: {str(e)}")
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}")
            return Response({'error': 'Processing error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def stripe_config(request):
    """Get Stripe publishable key for frontend"""
    return Response({
        'publishableKey': settings.STRIPE_PUBLISHABLE_KEY,
    })
