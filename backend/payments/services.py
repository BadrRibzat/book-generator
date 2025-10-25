import os
import stripe
from django.conf import settings
from django.utils import timezone
from .models import Subscription, SubscriptionPlan, Payment, WebhookEvent
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    """Service class for handling Stripe operations"""

    @staticmethod
    def create_customer(user):
        """Create a Stripe customer for the user"""
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.username,
                metadata={
                    'user_id': user.id,
                    'username': user.username
                }
            )
            return customer
        except Exception as e:
            logger.error(f"Failed to create Stripe customer for user {user.id}: {str(e)}")
            raise

    @staticmethod
    def create_subscription(user, plan, payment_method_id=None):
        """Create a subscription for the user"""
        try:
            # Get or create customer
            subscription = Subscription.objects.filter(user=user).first()
            if not subscription or not subscription.stripe_customer_id:
                customer = StripeService.create_customer(user)
                customer_id = customer.id

                # Update or create subscription record
                if subscription:
                    subscription.stripe_customer_id = customer_id
                    subscription.save()
                else:
                    subscription = Subscription.objects.create(
                        user=user,
                        plan=plan,
                        stripe_customer_id=customer_id,
                        status='incomplete'
                    )
            else:
                customer_id = subscription.stripe_customer_id

            # Create subscription data
            subscription_data = {
                'customer': customer_id,
                'items': [{
                    'price': plan.stripe_price_id,
                }],
                'metadata': {
                    'user_id': user.id,
                    'plan_id': plan.id,
                },
                'payment_behavior': 'default_incomplete',
                'expand': ['latest_invoice.payment_intent'],
            }

            if payment_method_id:
                # Attach payment method to customer
                stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)
                stripe.Customer.modify(customer_id, invoice_settings={
                    'default_payment_method': payment_method_id
                })

            # Create the subscription
            stripe_subscription = stripe.Subscription.create(**subscription_data)

            # Update our subscription record
            subscription.stripe_subscription_id = stripe_subscription.id
            subscription.status = stripe_subscription.status
            subscription.current_period_start = timezone.datetime.fromtimestamp(
                stripe_subscription.current_period_start
            )
            subscription.current_period_end = timezone.datetime.fromtimestamp(
                stripe_subscription.current_period_end
            )
            subscription.save()

            return {
                'subscription': subscription,
                'stripe_subscription': stripe_subscription,
                'client_secret': stripe_subscription.latest_invoice.payment_intent.client_secret
            }

        except Exception as e:
            logger.error(f"Failed to create subscription for user {user.id}: {str(e)}")
            raise

    @staticmethod
    def cancel_subscription(subscription):
        """Cancel a user's subscription"""
        try:
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=True
            )

            subscription.cancel_at_period_end = True
            subscription.save()

            return True
        except Exception as e:
            logger.error(f"Failed to cancel subscription {subscription.id}: {str(e)}")
            raise

    @staticmethod
    def reactivate_subscription(subscription):
        """Reactivate a canceled subscription"""
        try:
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=False
            )

            subscription.cancel_at_period_end = False
            subscription.save()

            return True
        except Exception as e:
            logger.error(f"Failed to reactivate subscription {subscription.id}: {str(e)}")
            raise

    @staticmethod
    def update_subscription_plan(subscription, new_plan):
        """Update subscription to a different plan"""
        try:
            # Get current subscription item
            stripe_subscription = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
            subscription_item_id = stripe_subscription['items']['data'][0]['id']

            # Update the subscription item
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                items=[{
                    'id': subscription_item_id,
                    'price': new_plan.stripe_price_id,
                }],
                metadata={
                    'user_id': subscription.user.id,
                    'plan_id': new_plan.id,
                }
            )

            # Update our record
            subscription.plan = new_plan
            subscription.save()

            return True
        except Exception as e:
            logger.error(f"Failed to update subscription {subscription.id}: {str(e)}")
            raise

    @staticmethod
    def handle_webhook_event(event_data):
        """Process Stripe webhook events"""
        try:
            event_type = event_data['type']
            event_id = event_data['id']

            # Check if we've already processed this event
            if WebhookEvent.objects.filter(stripe_event_id=event_id).exists():
                logger.info(f"Webhook event {event_id} already processed")
                return

            # Save the event
            WebhookEvent.objects.create(
                stripe_event_id=event_id,
                event_type=event_type,
                data=event_data,
                processed=False
            )

            # Process based on event type
            if event_type == 'customer.subscription.updated':
                StripeService._handle_subscription_updated(event_data['data']['object'])
            elif event_type == 'customer.subscription.deleted':
                StripeService._handle_subscription_deleted(event_data['data']['object'])
            elif event_type == 'invoice.payment_succeeded':
                StripeService._handle_payment_succeeded(event_data['data']['object'])
            elif event_type == 'invoice.payment_failed':
                StripeService._handle_payment_failed(event_data['data']['object'])

            # Mark as processed
            WebhookEvent.objects.filter(stripe_event_id=event_id).update(processed=True)

        except Exception as e:
            logger.error(f"Failed to process webhook event {event_id}: {str(e)}")
            raise

    @staticmethod
    def _handle_subscription_updated(stripe_subscription):
        """Handle subscription updated webhook"""
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription['id']
            )

            subscription.status = stripe_subscription['status']
            subscription.current_period_start = timezone.datetime.fromtimestamp(
                stripe_subscription['current_period_start']
            )
            subscription.current_period_end = timezone.datetime.fromtimestamp(
                stripe_subscription['current_period_end']
            )
            subscription.cancel_at_period_end = stripe_subscription.get('cancel_at_period_end', False)
            subscription.save()

            logger.info(f"Updated subscription {subscription.id} status to {subscription.status}")

        except Subscription.DoesNotExist:
            logger.warning(f"Subscription {stripe_subscription['id']} not found in database")

    @staticmethod
    def _handle_subscription_deleted(stripe_subscription):
        """Handle subscription deleted webhook"""
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription['id']
            )
            subscription.status = 'canceled'
            subscription.save()

            logger.info(f"Marked subscription {subscription.id} as canceled")

        except Subscription.DoesNotExist:
            logger.warning(f"Subscription {stripe_subscription['id']} not found in database")

    @staticmethod
    def _handle_payment_succeeded(invoice):
        """Handle successful payment webhook"""
        try:
            # Create payment record
            if invoice.get('subscription'):
                subscription = Subscription.objects.get(
                    stripe_subscription_id=invoice['subscription']
                )

                Payment.objects.create(
                    user=subscription.user,
                    payment_type='subscription',
                    subscription=subscription,
                    amount=invoice['amount_paid'] / 100,  # Convert from cents
                    currency=invoice['currency'],
                    status='succeeded',
                    metadata=invoice
                )

                logger.info(f"Recorded successful payment for subscription {subscription.id}")

        except Exception as e:
            logger.error(f"Failed to handle payment succeeded: {str(e)}")

    @staticmethod
    def _handle_payment_failed(invoice):
        """Handle failed payment webhook"""
        try:
            if invoice.get('subscription'):
                subscription = Subscription.objects.get(
                    stripe_subscription_id=invoice['subscription']
                )

                Payment.objects.create(
                    user=subscription.user,
                    payment_type='subscription',
                    subscription=subscription,
                    amount=invoice['amount_due'] / 100,  # Convert from cents
                    currency=invoice['currency'],
                    status='failed',
                    metadata=invoice
                )

                logger.info(f"Recorded failed payment for subscription {subscription.id}")

        except Exception as e:
            logger.error(f"Failed to handle payment failed: {str(e)}")

    @staticmethod
    def get_subscription_plans():
        """Get all active subscription plans"""
        return SubscriptionPlan.objects.filter(is_active=True).order_by('price')

    @staticmethod
    def get_user_subscription(user):
        """Get user's current subscription"""
        return Subscription.objects.filter(user=user).first()