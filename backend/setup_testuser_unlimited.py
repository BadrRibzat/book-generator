#!/usr/bin/env python
"""
Setup script to give testuser unlimited book generation for testing
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

def setup_testuser_unlimited():
    """
    Configure testuser with unlimited book generation capabilities
    """
    print("=" * 60)
    print("Setting up testuser with unlimited book generation...")
    print("=" * 60)
    
    try:
        # Get testuser
        testuser = User.objects.get(username='testuser')
        print(f"✓ Found testuser: {testuser.email}")
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=testuser)
        
        if created:
            print("✓ Created new UserProfile for testuser")
        else:
            print("✓ Using existing UserProfile")
        
        # Update profile with unlimited settings
        profile.subscription_tier = 'testing'  # Special testing tier
        profile.subscription_status = 'active'
        profile.books_per_month = 999999  # Unlimited books
        profile.books_used_this_month = 0  # Reset usage
        
        # Update user details
        profile.full_name = "Test User"
        profile.billing_email = testuser.email
        
        profile.save()
        
        print("\n" + "=" * 60)
        print("✓ SUCCESS: testuser configured with unlimited access")
        print("=" * 60)
        print(f"Username: {testuser.username}")
        print(f"Email: {testuser.email}")
        print(f"Subscription Tier: {profile.subscription_tier}")
        print(f"Subscription Status: {profile.subscription_status}")
        print(f"Books Per Month: {profile.books_per_month} (UNLIMITED)")
        print(f"Books Used This Month: {profile.books_used_this_month}")
        print("=" * 60)
        print("\n✓ testuser can now create unlimited books for testing!\n")
        
        return True
        
    except User.DoesNotExist:
        print("\n✗ ERROR: testuser not found!")
        print("Please create testuser first with:")
        print("  Email: testuser@example.com")
        print("  Password: test123")
        return False
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = setup_testuser_unlimited()
    sys.exit(0 if success else 1)
