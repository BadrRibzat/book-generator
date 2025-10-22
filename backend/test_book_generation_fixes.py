#!/usr/bin/env python
"""
Test script to verify book generation fixes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.services.book_generator import BookGeneratorProfessional
from books.models import Book
from django.contrib.auth.models import User

def test_title_extraction():
    """Test that title extraction works with markdown formatting"""
    generator = BookGeneratorProfessional()
    
    test_content = """# **Title:** *Automation Alchemy: Transforming Chaos into Efficiency with Smart Workflows*
**Subtitle:** *Build Future-Ready Systems with Low-Code Tools, AI Integration, and Ethical Design*

---

### **Back-Cover Blurb (75 words)**  
In a world drowning in repetitive tasks..."""
    
    title = generator.extract_title(test_content)
    print(f"✓ Title extraction test: {title}")
    assert title == "Automation Alchemy: Transforming Chaos into Efficiency with Smart Workflows", f"Expected correct title, got: {title}"
    print("✓ Title extraction working correctly\n")


def test_parse_book_content():
    """Test that book content is properly parsed into chapters"""
    generator = BookGeneratorProfessional()
    
    test_content = """# Title: Test Book

## Chapter 1: Introduction

This is the introduction content.

## Chapter 2: Main Content

This is the main content.

More paragraphs here.
"""
    
    parsed = generator.parse_book_content(test_content, 20)
    print(f"✓ Parse test - Found {len(parsed.get('chapters', []))} chapters")
    print(f"  Chapters: {[ch.get('title', 'No title') for ch in parsed.get('chapters', [])]}")
    assert len(parsed.get('chapters', [])) > 0, "Should have parsed chapters"
    print("✓ Content parsing working\n")


def test_latest_book_structure():
    """Check the latest book in database"""
    latest = Book.objects.order_by('-created_at').first()
    
    if not latest:
        print("⚠ No books in database to test")
        return
    
    print(f"Latest book in database:")
    print(f"  ID: {latest.id}")
    print(f"  Title: {latest.title}")
    print(f"  Status: {latest.status}")
    print(f"  Page length: {latest.page_length}")
    
    # Check MongoDB content
    from backend.utils.mongodb import get_mongodb_db
    db = get_mongodb_db()
    
    if latest.mongodb_id:
        from bson import ObjectId
        content = db.book_contents.find_one({'_id': ObjectId(latest.mongodb_id)})
        if content:
            content_data = content.get('content', {})
            print(f"\n  MongoDB content:")
            print(f"    Has 'chapters' key: {'chapters' in content_data}")
            print(f"    Has 'content' key: {'content' in content_data}")
            
            if isinstance(content_data, dict):
                print(f"    Keys: {list(content_data.keys())}")
                if 'chapters' in content_data:
                    print(f"    Number of chapters: {len(content_data['chapters'])}")
                else:
                    print(f"    ⚠ WARNING: No 'chapters' key found - PDF will be empty!")
            
            # Test PDF creation with this data
            if 'chapters' not in content_data and 'content' in content_data:
                print(f"\n  Testing parse on existing content...")
                generator = BookGeneratorProfessional()
                raw_content = content_data.get('content', '')
                if isinstance(raw_content, str):
                    parsed = generator.parse_book_content(raw_content, latest.page_length)
                    print(f"    Parsed chapters: {len(parsed.get('chapters', []))}")
    
    print()


if __name__ == '__main__':
    print("=" * 60)
    print("BOOK GENERATION FIXES TEST")
    print("=" * 60)
    print()
    
    try:
        test_title_extraction()
        test_parse_book_content()
        test_latest_book_structure()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("Key fixes verified:")
        print("1. ✓ Title extraction handles markdown formatting")
        print("2. ✓ Content parsing into chapters works")
        print("3. ✓ Database structure checked")
        print()
        print("⚠ NOTE: Existing books in DB need regeneration")
        print("   Old books don't have 'chapters' key and will produce empty PDFs")
        print()
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
