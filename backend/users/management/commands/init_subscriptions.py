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
                'name': 'Free Tier',
                'description': 'Everyone starts here - 2 books per month with 5 limited niches',
                'price_monthly': 0.00,
                'price_annual': 0.00,
                'currency': 'USD',
                'max_books_per_month': 2,
                'max_pages_per_book': 15,
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
        
        # Parents Plan - $12/month
        parents_plan, created = SubscriptionPlan.objects.get_or_create(
            tier='parents',
            defaults={
                'name': 'For Parents',
                'description': 'Perfect for parents creating educational content for preschoolers',
                'price_monthly': 12.00,
                'price_annual': 144.00,  # No discount mentioned
                'currency': 'USD',
                'max_books_per_month': 8,
                'max_pages_per_book': 20,
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
            self.stdout.write(self.style.SUCCESS(f"Created Parents Plan: ${parents_plan.price_monthly}/month"))
        else:
            self.stdout.write(f"Parents Plan already exists: ${parents_plan.price_monthly}/month")

        # Creators Plan - $29/month
        creators_plan, created = SubscriptionPlan.objects.get_or_create(
            tier='creators',
            defaults={
                'name': 'For Creators',
                'description': 'For digital marketers and content creators needing high volume',
                'price_monthly': 29.00,
                'price_annual': 348.00,  # No discount mentioned
                'currency': 'USD',
                'max_books_per_month': 12,
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
            self.stdout.write(self.style.SUCCESS(f"Created Creators Plan: ${creators_plan.price_monthly}/month"))
        else:
            self.stdout.write(f"Creators Plan already exists: ${creators_plan.price_monthly}/month")



        # Update existing user profiles with default plan settings
        self.stdout.write("Updating user profiles with subscription limits...")
        
        profiles = UserProfile.objects.all()
        updated_count = 0
        
        for profile in profiles:
            # Set default books per month based on subscription tier
            if profile.subscription_tier == 'free':
                profile.books_per_month = 2
            elif profile.subscription_tier == 'parents':
                profile.books_per_month = 8
            elif profile.subscription_tier == 'creators':
                profile.books_per_month = 12
            
            # Generate referral code if not exists
            if not profile.referral_code:
                import random
                import string
                profile.referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            profile.save()
            updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} user profiles"))
        self.stdout.write(self.style.SUCCESS("Subscription initialization complete!"))
