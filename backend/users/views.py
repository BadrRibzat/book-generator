from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe

from .models import (
    UserProfile, 
    SubscriptionPlan, 
    UserActivity, 
    DownloadHistory, 
    Payment, 
    Subscription,
    Referral
)
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    SubscriptionPlanSerializer,
    UserActivitySerializer, 
    DownloadHistorySerializer, 
    PaymentSerializer,
    SubscriptionSerializer, 
    ReferralSerializer,
    UserAnalyticsSerializer,
    SubscriptionCreateSerializer,
    PaymentIntentSerializer,
    ReferralCreateSerializer,
    UserProfileUpdateSerializer,
    SubscriptionUpgradeSerializer,
    UsageReportSerializer
)

User = get_user_model()


class UserProfileViewSet(viewsets.ModelViewSet):
    """User profile management viewset"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get user analytics data"""
        profile = request.user.profile
        
        # Calculate analytics
        total_books = request.user.books.count()
        total_downloads = request.user.downloads.count()
        total_revenue = request.user.payments.filter(
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get monthly usage
        current_month = timezone.now().month
        current_year = timezone.now().year
        monthly_usage = request.user.books.filter(
            created_at__year=current_year,
            created_at__month=current_month
        ).count()
        
        # Get last activity
        last_activity = UserActivity.objects.filter(
            user=request.user
        ).first()
        
        analytics_data = {
            'total_books_created': total_books,
            'total_books_downloaded': total_downloads,
            'total_revenue': total_revenue,
            'monthly_usage': monthly_usage,
            'subscription_tier': profile.subscription_tier,
            'account_created_date': request.user.date_joined,
            'last_activity_date': last_activity.timestamp if last_activity else None
        }
        
        serializer = UserAnalyticsSerializer(analytics_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_profile(self, request):
        """Update user profile"""
        profile = request.user.profile
        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def usage_limits(self, request):
        """Get current usage limits"""
        profile = request.user.profile
        
        # Check if we need to reset daily usage
        profile.reset_daily_usage()
        
        return Response({
            'subscription_tier': profile.subscription_tier,
            'books_per_day': profile.books_per_day,
            'books_used_today': profile.books_used_today,
            'can_create_book': profile.can_create_book(),
            'reset_date': profile.daily_reset_date
        })


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Subscription plans viewset"""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """User activity tracking viewset"""
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return UserActivity.objects.filter(user=self.request.user).order_by('-timestamp')


class DownloadHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Download history viewset"""
    serializer_class = DownloadHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return DownloadHistory.objects.filter(user=self.request.user).order_by('-timestamp')


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment management viewset"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Subscription management viewset"""
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return Subscription.objects.filter(user=self.request.user).order_by('-started_at')
    
    @action(detail=False, methods=['post'])
    def create_subscription(self, request):
        """Create new subscription"""
        serializer = SubscriptionCreateSerializer(data=request.data)
        if serializer.is_valid():
            # This would integrate with Stripe
            # For now, we'll create a trial subscription
            plan_tier = serializer.validated_data['plan_tier']
            try:
                plan = SubscriptionPlan.objects.get(tier=plan_tier, is_active=True)
                
                # Create subscription
                subscription = Subscription.objects.create(
                    user=request.user,
                    plan=plan,
                    status='trial',
                    current_period_start=timezone.now(),
                    current_period_end=timezone.now() + timezone.timedelta(days=30),
                    notes='Trial subscription'
                )
                
                # Update user profile
                profile = request.user.profile
                profile.subscription_tier = plan_tier
                profile.subscription_status = 'active'
                profile.save()
                
                # Track activity
                UserActivity.objects.create(
                    user=request.user,
                    activity_type='subscription_upgrade',
                    description=f'Created {plan_tier} subscription'
                )
                
                return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
                
            except SubscriptionPlan.DoesNotExist:
                return Response(
                    {'error': 'Invalid subscription plan'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def upgrade_subscription(self, request):
        """Upgrade subscription"""
        serializer = SubscriptionUpgradeSerializer(data=request.data)
        if serializer.is_valid():
            new_plan_tier = serializer.validated_data['new_plan_tier']
            try:
                new_plan = SubscriptionPlan.objects.get(tier=new_plan_tier, is_active=True)
                
                # Get current subscription
                current_subscription = Subscription.objects.filter(
                    user=request.user,
                    status='active'
                ).first()
                
                if current_subscription:
                    # Cancel current subscription
                    current_subscription.status = 'cancelled'
                    current_subscription.cancelled_at = timezone.now()
                    current_subscription.save()
                
                # Create new subscription
                subscription = Subscription.objects.create(
                    user=request.user,
                    plan=new_plan,
                    status='active',
                    current_period_start=timezone.now(),
                    current_period_end=timezone.now() + timezone.timedelta(days=30),
                    notes=f'Upgraded to {new_plan_tier}'
                )
                
                # Update user profile
                profile = request.user.profile
                profile.subscription_tier = new_plan_tier
                profile.save()
                
                # Track activity
                UserActivity.objects.create(
                    user=request.user,
                    activity_type='subscription_upgrade',
                    description=f'Upgraded to {new_plan_tier} subscription'
                )
                
                return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
                
            except SubscriptionPlan.DoesNotExist:
                return Response(
                    {'error': 'Invalid subscription plan'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferralViewSet(viewsets.ModelViewSet):
    """Referral management viewset"""
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return Referral.objects.filter(referrer=self.request.user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def use_referral(self, request):
        """Use a referral code"""
        serializer = ReferralCreateSerializer(data=request.data)
        if serializer.is_valid():
            referral_code = serializer.validated_data['referral_code']
            try:
                referrer_profile = UserProfile.objects.get(referral_code=referral_code)
                
                # Create referral record
                referral = Referral.objects.create(
                    referrer=referrer_profile.user,
                    referee=request.user,
                    status='pending',
                    reward_amount=5.00,  # $5 reward
                    reward_currency='USD'
                )
                
                # Update referrer's referral count
                referrer_profile.referral_count += 1
                referrer_profile.save()
                
                # Track activity
                UserActivity.objects.create(
                    user=request.user,
                    activity_type='profile_update',
                    description=f'Used referral code: {referral_code}'
                )
                
                return Response(ReferralSerializer(referral).data, status=status.HTTP_201_CREATED)
                
            except UserProfile.DoesNotExist:
                return Response(
                    {'error': 'Invalid referral code'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def generate_code(self, request):
        """Generate referral code for user"""
        profile = request.user.profile
        
        if not profile.referral_code:
            import random
            import string
            profile.referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            profile.save()
        
        return Response({'referral_code': profile.referral_code})


class PaymentIntentView(APIView):
    """Create Stripe payment intent"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PaymentIntentSerializer(data=request.data)
        if serializer.is_valid():
            # This would integrate with Stripe
            # For now, return mock response
            return Response({
                'client_secret': 'mock_client_secret',
                'payment_intent_id': 'mock_intent_id'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsageReportView(APIView):
    """Generate usage reports"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = UsageReportSerializer(data=request.data)
        if serializer.is_valid():
            period = serializer.validated_data['period']
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            
            # Generate report based on period
            if period == 'daily':
                # Daily breakdown
                report = self._generate_daily_report(start_date, end_date)
            elif period == 'weekly':
                # Weekly breakdown
                report = self._generate_weekly_report(start_date, end_date)
            else:
                # Monthly breakdown
                report = self._generate_monthly_report(start_date, end_date)
            
            return Response(report)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _generate_daily_report(self, start_date, end_date):
        """Generate daily usage report"""
        books = request.user.books.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )
        
        report = {
            'period': 'daily',
            'date_range': {'start': start_date, 'end': end_date},
            'summary': {
                'total_books': books.count(),
                'successful_generations': books.filter(status='ready').count(),
                'failed_generations': books.filter(status='error').count(),
            },
            'daily_breakdown': []
        }
        
        # Add daily breakdown
        current_date = start_date
        while current_date <= end_date:
            day_books = books.filter(created_at__date=current_date)
            report['daily_breakdown'].append({
                'date': current_date,
                'books_count': day_books.count(),
                'status_distribution': dict(
                    day_books.values_list('status', flat=True)
                    .annotate(count=Count('id'))
                    .values_list('status', 'count')
                )
            })
            current_date += timezone.timedelta(days=1)
        
        return report
    
    def _generate_weekly_report(self, start_date, end_date):
        """Generate weekly usage report"""
        books = request.user.books.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )
        
        report = {
            'period': 'weekly',
            'date_range': {'start': start_date, 'end': end_date},
            'summary': {
                'total_books': books.count(),
                'successful_generations': books.filter(status='ready').count(),
                'failed_generations': books.filter(status='error').count(),
            },
            'weekly_breakdown': []
        }
        
        # Add weekly breakdown
        current_week_start = start_date - timezone.timedelta(days=start_date.weekday())
        while current_week_start <= end_date:
            current_week_end = current_week_start + timezone.timedelta(days=6)
            week_books = books.filter(
                created_at__date__gte=current_week_start,
                created_at__date__lte=current_week_end
            )
            
            report['weekly_breakdown'].append({
                'week_start': current_week_start,
                'week_end': current_week_end,
                'books_count': week_books.count(),
                'status_distribution': dict(
                    week_books.values_list('status', flat=True)
                    .annotate(count=Count('id'))
                    .values_list('status', 'count')
                )
            })
            
            current_week_start += timezone.timedelta(days=7)
        
        return report
    
    def _generate_monthly_report(self, start_date, end_date):
        """Generate monthly usage report"""
        books = request.user.books.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )
        
        report = {
            'period': 'monthly',
            'date_range': {'start': start_date, 'end': end_date},
            'summary': {
                'total_books': books.count(),
                'successful_generations': books.filter(status='ready').count(),
                'failed_generations': books.filter(status='error').count(),
            },
            'domain_distribution': dict(
                books.values_list('domain', flat=True)
                .annotate(count=Count('id'))
                .values_list('domain', 'count')
            ),
            'monthly_breakdown': []
        }
        
        # Add monthly breakdown
        current_month_start = start_date.replace(day=1)
        while current_month_start <= end_date:
            if current_month_start.month == 12:
                next_month = current_month_start.replace(year=current_month_start.year + 1, month=1)
            else:
                next_month = current_month_start.replace(month=current_month_start.month + 1)
            
            month_books = books.filter(
                created_at__date__gte=current_month_start,
                created_at__date__lt=next_month
            )
            
            report['monthly_breakdown'].append({
                'month': current_month_start.strftime('%Y-%m'),
                'books_count': month_books.count(),
                'status_distribution': dict(
                    month_books.values_list('status', flat=True)
                    .annotate(count=Count('id'))
                    .values_list('status', 'count')
                )
            })
            
            current_month_start = next_month
        
        return report


class DashboardView(APIView):
    """Dashboard overview"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get dashboard overview"""
        profile = request.user.profile
        
        # Reset monthly usage if needed
        profile.reset_daily_usage()
        
        # Get recent activity
        recent_activity = UserActivity.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:10]
        
        # Get recent books
        recent_books = request.user.books.order_by('-created_at')[:5]
        
        # Get subscription info
        current_subscription = Subscription.objects.filter(
            user=request.user,
            status='active'
        ).first()
        
        dashboard_data = {
            'user_profile': UserProfileSerializer(profile).data,
            'recent_activity': UserActivitySerializer(recent_activity, many=True).data,
            'recent_books': recent_books,
            'current_subscription': SubscriptionSerializer(current_subscription).data if current_subscription else None,
        }
        
        return Response(dashboard_data)
