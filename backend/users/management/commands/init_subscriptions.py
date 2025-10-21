from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import SubscriptionPlan, UserProfile


class Command(BaseCommand):
    help = 'Initialize subscription plans with default data'

    def handle(self, *args, **options):
        self.stdout.write("Initializing subscription plans...")
        
        # Free Plan - $0/month
        free_plan, created = SubscriptionPlan.objects.get_or_create(
            tier='free',
            defaults={
                'name': 'Free Plan',
                'description': 'Get started with basic book generation',
                'price_monthly': 0.00,
                'price_annual': 0.00,
                'currency': 'USD',
                'max_books_per_month': 30,  # 1 book per day = ~30 per month
                'max_pages_per_book': 30,
                'priority_generation': False,
                'commercial_license': False,
                'ai_enhancement': True,
                'custom_templates': False,
                'team_collaboration': False,
                'priority_support': False,
                'is_active': True,
                'sort_order': 0,
                'featured': False,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Free Plan: ${free_plan.price_monthly}/month"))
        else:
            self.stdout.write(f"Free Plan already exists: ${free_plan.price_monthly}/month")
        
        # Basic Plan - $15/month
        basic_plan, created = SubscriptionPlan.objects.get_or_create(
            tier='basic',
            defaults={
                'name': 'Basic Plan',
                'description': 'Perfect for individual creators starting their journey',
                'price_monthly': 15.00,
                'price_annual': 165.00,  # 15% discount
                'currency': 'USD',
                'max_books_per_month': 30,  # 1 book per day = ~30 per month
                'max_pages_per_book': 30,
                'priority_generation': False,
                'commercial_license': False,
                'ai_enhancement': True,
                'custom_templates': False,
                'team_collaboration': False,
                'priority_support': False,
                'is_active': True,
                'sort_order': 1,
                'featured': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Basic Plan: ${basic_plan.price_monthly}/month"))
        else:
            self.stdout.write(f"Basic Plan already exists: ${basic_plan.price_monthly}/month")

        # Premium Plan - $45/month
        premium_plan, created = SubscriptionPlan.objects.get_or_create(
            tier='premium',
            defaults={
                'name': 'Premium Plan',
                'description': 'For serious creators with higher volume needs',
                'price_monthly': 45.00,
                'price_annual': 495.00,  # 15% discount
                'currency': 'USD',
                'max_books_per_month': 90,  # 3 books per day = ~90 per month
                'max_pages_per_book': 30,
                'priority_generation': True,
                'commercial_license': True,
                'ai_enhancement': True,
                'custom_templates': True,
                'team_collaboration': False,
                'priority_support': True,
                'is_active': True,
                'sort_order': 2,
                'featured': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Premium Plan: ${premium_plan.price_monthly}/month"))
        else:
            self.stdout.write(f"Premium Plan already exists: ${premium_plan.price_monthly}/month")

        # Enterprise Plan - $60/month
        enterprise_plan, created = SubscriptionPlan.objects.get_or_create(
            tier='enterprise',
            defaults={
                'name': 'Enterprise Plan',
                'description': 'For power users and teams',
                'price_monthly': 60.00,
                'price_annual': 660.00,  # 15% discount
                'currency': 'USD',
                'max_books_per_month': 150,  # 5 books per day = ~150 per month
                'max_pages_per_book': 30,
                'priority_generation': True,
                'commercial_license': True,
                'ai_enhancement': True,
                'custom_templates': True,
                'team_collaboration': True,
                'priority_support': True,
                'is_active': True,
                'sort_order': 3,
                'featured': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Enterprise Plan: ${enterprise_plan.price_monthly}/month"))
        else:
            self.stdout.write(f"Enterprise Plan already exists: ${enterprise_plan.price_monthly}/month")

        # Update existing user profiles with default plan settings
        self.stdout.write("Updating user profiles with subscription limits...")
        
        profiles = UserProfile.objects.all()
        updated_count = 0
        
        for profile in profiles:
            # Set default books per day based on subscription tier
            if profile.subscription_tier == 'free':
                profile.books_per_day = 1
            elif profile.subscription_tier == 'basic':
                profile.books_per_day = 1
            elif profile.subscription_tier == 'premium':
                profile.books_per_day = 3
            elif profile.subscription_tier == 'enterprise':
                profile.books_per_day = 5
            
            # Generate referral code if not exists
            if not profile.referral_code:
                import random
                import string
                profile.referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            profile.save()
            updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} user profiles"))
        self.stdout.write(self.style.SUCCESS("Subscription initialization complete!"))
