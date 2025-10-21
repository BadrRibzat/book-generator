#!/usr/bin/env python
"""
Complete API Test Script
Tests the entire book generation flow end-to-end
"""

import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000/api"
USERS_BASE_URL = "http://127.0.0.1:8000/api/users"
session = requests.Session()

def print_step(step, message):
    """Print formatted step"""
    print(f"\n{'='*70}")
    print(f"Step {step}: {message}")
    print('='*70)

def test_registration():
    """Test user registration"""
    print_step(1, "Registering User")
    
    response = session.post(f"{USERS_BASE_URL}/auth/register/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password2": "testpass123"
    })
    
    if response.status_code == 201:
        data = response.json()
        print(f"✓ User registered: {data['user']['username']}")
        return True
    else:
        print(f"✗ Registration failed: {response.text}")
        return False

def test_login():
    """Test user login"""
    print_step(2, "Logging In User")
    
    response = session.post(f"{USERS_BASE_URL}/auth/login/", json={
        "username": "testuser",
        "password": "testpass123"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ User logged in: {data['user']['username']}")
        return True
    else:
        print(f"✗ Login failed: {response.text}")
        return False

def test_get_niches():
    """Test getting available sub-niches"""
    print_step(3, "Getting Available Sub-Niches")
    
    response = session.get("http://127.0.0.1:8000/api/config/sub-niches/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {len(data['domains'])} domains")
        for domain in data['domains']:
            niches = data['sub_niches'][domain['value']]
            print(f"  - {domain['label']}: {len(niches)} sub-niches")
        return True
    else:
        print(f"✗ Failed to get niches: {response.text}")
        return False

def test_create_book():
    """Test book creation"""
    print_step(4, "Creating Book")
    
    response = session.post("http://127.0.0.1:8000/api/books/", json={
        "domain": "ai_digital_transformation",
        "sub_niche": "ai_business_automation",
        "page_length": 15
    })
    
    if response.status_code == 201:
        book = response.json()
        print(f"✓ Book created!")
        print(f"  ID: {book['id']}")
        print(f"  Title: {book['title']}")
        print(f"  Status: {book['status']}")
        print(f"  Page Length: {book['page_length']}")
        return book['id']
    else:
        print(f"✗ Book creation failed: {response.text}")
        return None

def wait_for_covers(book_id, max_wait=120):
    """Wait for content generation and cover creation"""
    print_step(5, "Waiting for Content Generation & Cover Creation")
    
    start_time = time.time()
    dots = 0
    
    while time.time() - start_time < max_wait:
        response = session.get(f"http://127.0.0.1:8000/api/books/{book_id}/")
        
        if response.status_code != 200:
            print(f"\n✗ Failed to get book status: {response.text}")
            return False
        
        book = response.json()
        elapsed = int(time.time() - start_time)
        
        # Show progress
        sys.stdout.write(f"\r  Status: {book['status']} {'.' * (dots % 4)}{' ' * (3 - dots % 4)} ({elapsed}s)")
        sys.stdout.flush()
        dots += 1
        
        if book['status'] == 'cover_pending':
            print(f"\n✓ Content generated successfully!")
            print(f"  Covers available: {len(book['covers'])}")
            for cover in book['covers']:
                print(f"    - {cover['template_style']} (ID: {cover['id']})")
            return book['covers']
        
        elif book['status'] == 'error':
            print(f"\n✗ Generation error: {book.get('error_message', 'Unknown error')}")
            return False
        
        time.sleep(3)
    
    print(f"\n✗ Timeout waiting for book generation")
    return False

def test_select_cover(book_id, covers):
    """Test cover selection"""
    print_step(6, "Selecting Cover")
    
    if not covers:
        print("✗ No covers available")
        return False
    
    cover_id = covers[0]['id']
    print(f"  Selecting cover: {covers[0]['template_style']} (ID: {cover_id})")
    
    response = session.post(f"http://127.0.0.1:8000/api/books/{book_id}/select_cover/", json={
        "cover_id": cover_id
    })
    
    if response.status_code == 200:
        book = response.json()
        print(f"✓ Cover selected!")
        print(f"  Status: {book['status']}")
        print(f"  Can download: {book['can_download']}")
        print(f"  Download URL: {book['download_url']}")
        return True
    else:
        print(f"✗ Cover selection failed: {response.text}")
        return False

def test_download_book(book_id):
    """Test book download"""
    print_step(7, "Downloading Book")
    
    response = session.get(f"http://127.0.0.1:8000/api/books/{book_id}/download/")
    
    if response.status_code == 200:
        filename = f"test_book_{book_id}.pdf"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        file_size = len(response.content) / 1024  # KB
        print(f"✓ Book downloaded successfully!")
        print(f"  Filename: {filename}")
        print(f"  Size: {file_size:.1f} KB")
        print(f"\n  Open the file to verify:")
        print(f"  - Cover on page 1")
        print(f"  - Content on following pages")
        return True
    else:
        print(f"✗ Download failed: {response.text}")
        return False

def test_book_history():
    """Test getting book history"""
    print_step(8, "Getting Book History")
    
    response = session.get("http://127.0.0.1:8000/api/books/")
    
    if response.status_code == 200:
        books = response.json()
        print(f"✓ Found {len(books)} book(s)")
        for book in books:
            print(f"  - {book['title']} ({book['status']})")
        return True
    else:
        print(f"✗ Failed to get history: {response.text}")
        return False

def main():
    """Run complete test suite"""
    print("\n" + "="*70)
    print("BOOK GENERATOR API - COMPLETE TEST")
    print("="*70)
    print(f"\nBase URL: {BASE_URL}")
    print("Make sure Django server is running: python manage.py runserver")
    print("\nPress Ctrl+C to cancel...")
    
    time.sleep(2)
    
    try:
        # Run tests
        if not test_registration():
            return False
        
        if not test_login():
            return False
        
        if not test_get_niches():
            return False
        
        book_id = test_create_book()
        if not book_id:
            return False
        
        covers = wait_for_covers(book_id)
        if not covers:
            return False
        
        if not test_select_cover(book_id, covers):
            return False
        
        if not test_download_book(book_id):
            return False
        
        if not test_book_history():
            return False
        
        # Success!
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\nYour book generator is working perfectly!")
        print("Next steps:")
        print("  1. Check the downloaded PDF")
        print("  2. Try other sub-niches")
        print("  3. Build the frontend (Vue)")
        print("  4. Deploy to production")
        print("\n")
        return True
        
    except KeyboardInterrupt:
        print("\n\n✗ Test cancelled by user")
        return False
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
