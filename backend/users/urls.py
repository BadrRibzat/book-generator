from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    SubscriptionPlanViewSet,
    UserActivityViewSet,
    DownloadHistoryViewSet,
    PaymentViewSet,
    SubscriptionViewSet,
    ReferralViewSet,
    PaymentIntentView,
    UsageReportView,
    DashboardView
)
# Import authentication views from books app
from books.views import current_user, register_user, login_user, logout_user

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'subscription-plans', SubscriptionPlanViewSet, basename='subscriptionplan')
router.register(r'activities', UserActivityViewSet, basename='useractivity')
router.register(r'downloads', DownloadHistoryViewSet, basename='download')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'referrals', ReferralViewSet, basename='referral')

urlpatterns = [
    path('', include(router.urls)),
    
    # Clear authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
    path('profile/', current_user, name='current-user-profile'),  # Replace /me with /profile
    
    # SaaS specific endpoints
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('payment-intent/', PaymentIntentView.as_view(), name='payment-intent'),
    path('usage-report/', UsageReportView.as_view(), name='usage-report'),
]
