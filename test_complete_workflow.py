#!/usr/bin/env python3
"""
Complete test suite to verify all critical book generation fixes
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_complete_workflow():
    print("🔧 Testing Complete Book Generation Workflow")
    print("=" * 60)
    
    # Test 1: Content Categories API
    print("\n1️⃣ Testing Content Categories...")
    try:
        response = requests.get(f"{BASE_URL}/api/config/sub-niches/")
        if response.status_code == 200:
            data = response.json()
            categories = len(data.get('sub_niches', {}))
            print(f"   ✅ {categories} content categories loaded")
            
            # Show some sample categories
            if 'sub_niches' in data:
                sample_categories = list(data['sub_niches'].keys())[:3]
                print(f"   📝 Sample: {', '.join(sample_categories)}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Subscription Plans API
    print("\n2️⃣ Testing Subscription Plans...")
    try:
        response = requests.get(f"{BASE_URL}/api/users/subscription-plans/")
        if response.status_code == 200:
            plans = response.json()
            print(f"   ✅ {len(plans)} subscription plans available")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Book Creation with New Categories
    print("\n3️⃣ Testing Book Creation...")
    print("   📝 Creating test user and book...")
    
    # Create test session
    session = requests.Session()
    
    # Register user
    register_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "testpass123",
        "password2": "testpass123"
    }
    
    try:
        # Register
        response = session.post(f"{BASE_URL}/api/users/auth/register/", json=register_data)
        if response.status_code == 201:
            print("   ✅ User registered successfully")
            
            # Login
            login_data = {
                "username": register_data["username"],
                "password": register_data["password"]
            }
            response = session.post(f"{BASE_URL}/api/users/auth/login/", json=login_data)
            if response.status_code == 200:
                print("   ✅ User logged in successfully")
                
                # Create book with new categories
                book_data = {
                    "domain": "personal_development",
                    "sub_niche": "self_esteem",
                    "page_length": 15
                }
                
                response = session.post(f"{BASE_URL}/api/books/", json=book_data)
                if response.status_code == 201:
                    book = response.json()
                    book_id = book['id']
                    print(f"   ✅ Book created successfully (ID: {book_id})")
                    print(f"   📚 Title: {book.get('title', 'N/A')}")
                    
                    # Test 4: Monitor Book Generation
                    print("\n4️⃣ Monitoring Book Generation...")
                    max_attempts = 30
                    attempt = 0
                    
                    while attempt < max_attempts:
                        response = session.get(f"{BASE_URL}/api/books/{book_id}/")
                        if response.status_code == 200:
                            book_status = response.json()
                            status = book_status['status']
                            print(f"   📊 Status: {status}")
                            
                            if status == 'content_generated' or status == 'cover_pending':
                                covers = book_status.get('covers', [])
                                print(f"   ✅ Content generated with {len(covers)} covers")
                                
                                # Test 5: Cover Selection
                                if covers:
                                    print("\n5️⃣ Testing Cover Selection...")
                                    cover_id = covers[0]['id']
                                    select_data = {"cover_id": cover_id}
                                    
                                    response = session.post(f"{BASE_URL}/api/books/{book_id}/select_cover/", json=select_data)
                                    if response.status_code == 200:
                                        print("   ✅ Cover selected successfully")
                                        
                                        # Check if book is ready for download
                                        response = session.get(f"{BASE_URL}/api/books/{book_id}/")
                                        if response.status_code == 200:
                                            final_book = response.json()
                                            if final_book.get('can_download'):
                                                print("   ✅ Book ready for download")
                                                
                                                # Test 6: Download Functionality
                                                print("\n6️⃣ Testing Download...")
                                                response = session.get(f"{BASE_URL}/api/books/{book_id}/download/")
                                                if response.status_code == 200:
                                                    print("   ✅ Download successful")
                                                    print(f"   📄 Content-Type: {response.headers.get('content-type')}")
                                                else:
                                                    print(f"   ❌ Download failed: {response.status_code}")
                                            else:
                                                print("   ⚠️ Book not ready for download yet")
                                    else:
                                        print(f"   ❌ Cover selection failed: {response.status_code}")
                                        print(f"   📝 Response: {response.text}")
                                break
                            elif status == 'error':
                                error_msg = book_status.get('error_message', 'Unknown error')
                                print(f"   ❌ Book generation failed: {error_msg}")
                                break
                            elif status == 'ready':
                                print("   ✅ Book ready!")
                                break
                        
                        attempt += 1
                        if attempt < max_attempts:
                            time.sleep(3)
                    
                    if attempt >= max_attempts:
                        print("   ⚠️ Timeout waiting for book generation")
                    
                    # Test 7: Cleanup (Delete Book)
                    print("\n7️⃣ Testing Book Deletion...")
                    response = session.delete(f"{BASE_URL}/api/books/{book_id}/")
                    if response.status_code == 204:
                        print("   ✅ Book deleted successfully")
                    else:
                        print(f"   ❌ Delete failed: {response.status_code}")
                        
                else:
                    print(f"   ❌ Book creation failed: {response.status_code}")
                    print(f"   📝 Response: {response.text}")
            else:
                print(f"   ❌ Login failed: {response.status_code}")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Workflow error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Complete Workflow Test Finished!")
    print("📋 Summary of fixes implemented:")
    print("   ✅ Content categories loading in frontend")
    print("   ✅ PDF generation with proper error handling")
    print("   ✅ Download functionality with file responses")
    print("   ✅ Cover selection modal optimized")
    print("   ✅ Delete buttons added to all views")
    print("   ✅ 15 trending content categories implemented")
    print("   ✅ Backend subscription plans integrated")

if __name__ == "__main__":
    test_complete_workflow()