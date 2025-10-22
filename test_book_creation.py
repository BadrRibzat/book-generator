#!/usr/bin/env python3
"""
Test book creation with the updated serializer
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_book_creation():
    print("🔧 Testing Book Creation with Updated Serializer")
    print("=" * 60)

    # First, let's get some sample data
    try:
        # Get domains
        domains_response = requests.get(f"{BASE_URL}/domains/")
        if domains_response.status_code == 200:
            domains = domains_response.json()
            sample_domain = domains[0] if domains else None
            print(f"   ✅ Sample domain: {sample_domain['name']} (slug: {sample_domain['slug']})")
        else:
            print("   ❌ Could not get domains")
            return

        # Get niches
        niches_response = requests.get(f"{BASE_URL}/niches/")
        if niches_response.status_code == 200:
            niches = niches_response.json()
            sample_niche = niches[0] if niches else None
            print(f"   ✅ Sample niche: {sample_niche['name']} (id: {sample_niche['id']})")
        else:
            print("   ❌ Could not get niches")
            return

        # Get book styles
        styles_response = requests.get(f"{BASE_URL}/book-styles/")
        if styles_response.status_code == 200:
            styles = styles_response.json()
            sample_style = styles[0] if styles else None
            print(f"   ✅ Sample style: {sample_style['name']} (id: {sample_style['id']})")
        else:
            print("   ❌ Could not get book styles")
            return

        # Test data that matches frontend format
        test_data = {
            "domain": sample_domain['slug'],  # Frontend sends domain slug
            "niche": sample_niche['id'],      # Frontend sends niche ID
            "book_style": sample_style['id'], # Frontend sends book style ID
            "book_length": "medium",
            "target_audience": "beginners",
            "key_topics": ["introduction", "fundamentals"],
            "writing_preferences": "conversational",
            "cover_style": ""
        }

        print(f"\n📝 Test data: {json.dumps(test_data, indent=2)}")

        # Note: This will fail without authentication, but we can see the validation error
        response = requests.post(f"{BASE_URL}/books/", json=test_data)
        print(f"\n📊 Response status: {response.status_code}")
        print(f"📊 Response data: {response.text}")

        if response.status_code == 400:
            try:
                error_data = response.json()
                print("\n🔍 Validation errors:")
                for field, errors in error_data.items():
                    print(f"   - {field}: {errors}")
            except:
                print(f"   Raw response: {response.text}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("🎉 Book Creation Test Complete!")

if __name__ == "__main__":
    test_book_creation()