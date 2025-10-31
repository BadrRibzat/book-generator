#!/usr/bin/env python
"""
Simple Test for 3-Cover Generation System
"""

import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000/api"
session = requests.Session()

def test_login():
    """Login with testuser credentials"""
    print("🔐 Logging in...")
    
    response = session.post(f"{BASE_URL}/users/auth/login/", json={
        "username": "testuser",
        "password": "test123"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Logged in as: {data['user']['username']}")
        return True
    else:
        print(f"❌ Login failed: {response.text}")
        return False

def test_get_domains():
    """Get available domains"""
    print("📚 Getting domains...")
    
    response = session.get(f"{BASE_URL}/domains/")
    
    if response.status_code == 200:
        domains = response.json()
        print(f"✅ Found {len(domains)} domains")
        return domains
    else:
        print(f"❌ Failed to get domains: {response.text}")
        return None

def test_get_niches():
    """Get available niches"""
    print("🎯 Getting niches...")
    
    response = session.get(f"{BASE_URL}/niches/")
    
    if response.status_code == 200:
        niches = response.json()
        print(f"✅ Found {len(niches)} niches")
        return niches
    else:
        print(f"❌ Failed to get niches: {response.text}")
        return None

def test_create_book():
    """Create a book"""
    print("📖 Creating book...")
    
    # Get first domain
    domains = test_get_domains()
    if not domains:
        return None
    
    domain_slug = domains[0]['slug']
    
    # Get niches for this domain
    response = session.get(f"{BASE_URL}/niches/?domain={domain_slug}")
    if response.status_code != 200:
        print(f"❌ Failed to get niches for domain: {response.text}")
        return None
    
    domain_niches = response.json()
    if not domain_niches:
        print("❌ No niches found for domain")
        return None
    
    niche_id = domain_niches[0]['id']
    
    response = session.post(f"{BASE_URL}/books/", json={
        "domain": domain_slug,
        "niche": niche_id,
        "book_length": "standard"
    })
    
    if response.status_code == 201:
        book = response.json()
        print(f"✅ Book created: {book['title']} (ID: {book['id']})")
        return book
    else:
        print(f"❌ Book creation failed: {response.text}")
        return None

def wait_for_covers(book_id, max_wait=60):
    """Wait for covers to be generated"""
    print("🎨 Waiting for 3 covers to be generated...")
    
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        response = session.get(f"{BASE_URL}/books/{book_id}/")
        
        if response.status_code != 200:
            print(f"❌ Failed to get book: {response.text}")
            return None
        
        book = response.json()
        elapsed = int(time.time() - start_time)
        
        if book['status'] == 'cover_pending':
            covers = book.get('covers', [])
            if len(covers) >= 3:
                print(f"✅ 3 covers generated in {elapsed}s!")
                for i, cover in enumerate(covers):
                    print(f"   {i+1}. {cover['template_style']} style")
                return covers
            else:
                print(f"⏳ Status: {book['status']} - {len(covers)} covers so far ({elapsed}s)")
        
        elif book['status'] == 'error':
            print(f"❌ Generation error: {book.get('error_message', 'Unknown error')}")
            return None
        
        time.sleep(2)
    
    print("⏰ Timeout waiting for covers")
    return None

def test_select_cover(book_id, covers):
    """Select the first cover"""
    print("🎯 Selecting first cover...")
    
    cover_id = covers[0]['id']
    style = covers[0]['template_style']
    
    response = session.post(f"{BASE_URL}/books/{book_id}/select_cover/", json={
        "cover_id": cover_id
    })
    
    if response.status_code == 200:
        book = response.json()
        print(f"✅ Selected {style} cover!")
        print(f"   Status: {book['status']}")
        return book
    else:
        print(f"❌ Cover selection failed: {response.text}")
        return None

def main():
    """Test the 3-cover generation system"""
    print("🧪 Testing 3-Cover Generation System")
    print("=" * 50)
    
    # Login
    if not test_login():
        return False
    
    # Create book
    book = test_create_book()
    if not book:
        return False
    
    book_id = book['id']
    
    # Wait for covers
    covers = wait_for_covers(book_id)
    if not covers:
        return False
    
    # Verify we have 3 covers
    if len(covers) != 3:
        print(f"❌ Expected 3 covers, got {len(covers)}")
        return False
    
    print("✅ All 3 cover styles generated:")
    styles = [cover['template_style'] for cover in covers]
    print(f"   Styles: {', '.join(styles)}")
    
    # Select cover
    result = test_select_cover(book_id, covers)
    if not result:
        return False
    
    print("\n🎉 SUCCESS! 3-Cover Generation System Working!")
    print("✅ Login ✓ Book Creation ✓ 3 Cover Generation ✓ Cover Selection")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
