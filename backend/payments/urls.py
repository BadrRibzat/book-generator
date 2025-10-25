from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Subscription plans
    path('plans/', views.SubscriptionPlanListView.as_view(), name='subscription-plans'),

    # User subscription management
    path('subscription/', views.UserSubscriptionView.as_view(), name='user-subscription'),
    path('subscription/create/', views.CreateSubscriptionView.as_view(), name='create-subscription'),
    path('subscription/cancel/', views.CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('subscription/reactivate/', views.ReactivateSubscriptionView.as_view(), name='reactivate-subscription'),
    path('subscription/update/', views.UpdateSubscriptionView.as_view(), name='update-subscription'),

    # Payment history
    path('payments/', views.PaymentHistoryView.as_view(), name='payment-history'),

    # Stripe configuration
    path('config/', views.stripe_config, name='stripe-config'),

    # Webhooks
    path('webhook/', views.StripeWebhookView.as_view(), name='stripe-webhook'),
]