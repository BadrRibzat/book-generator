"""
Quick Test Script for Custom LLM Integration
Run this to verify your setup is working
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, '/home/badr/book-generator/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from customllm.integration import LLMIntegration


def test_integration():
    """Test the LLM integration selector"""
    print("\n" + "="*60)
    print("🧪 TESTING CUSTOM LLM INTEGRATION")
    print("="*60 + "\n")
    
    try:
        # Initialize integration
        print("1️⃣ Initializing LLM Integration...")
        llm = LLMIntegration()
        
        # Get service info
        info = llm.get_service_info()
        print(f"\n✅ Service Active: {info['service']}")
        print(f"   Rate Limited: {info['rate_limited']}")
        print(f"   Cost Model: {info['cost_model']}")
        print(f"   Status: {info['status']}")
        
        # Test outline generation
        print("\n2️⃣ Testing Outline Generation...")
        book_context = {
            'domain': 'AI & Automation',
            'niche': 'No-Code AI Tools',
            'audience': 'beginners',
            'page_count': 20,
            'title': 'Getting Started with No-Code AI'
        }
        
        outline_result = llm.generate_outline(book_context)
        
        print(f"\n✅ Outline Generated!")
        print(f"   Title: {outline_result.get('outline', {}).get('title', 'N/A')}")
        print(f"   Chapters: {outline_result.get('chapters', 0)}")
        print(f"   Model: {outline_result.get('metadata', {}).get('model', 'unknown')}")
        print(f"   Time: {outline_result.get('metadata', {}).get('elapsed_time', 0):.2f}s")
        
        # Test chapter generation
        print("\n3️⃣ Testing Chapter Generation...")
        chapter_result = llm.generate_chapter(
            chapter_title="Introduction to No-Code AI",
            chapter_outline="Brief overview of no-code AI tools and their benefits",
            book_context=book_context,
            word_count=300
        )
        
        print(f"\n✅ Chapter Generated!")
        print(f"   Word Count: {chapter_result.get('word_count', 0)}")
        print(f"   Model: {chapter_result.get('metadata', {}).get('model', 'unknown')}")
        print(f"   Time: {chapter_result.get('metadata', {}).get('elapsed_time', 0):.2f}s")
        print(f"   Preview: {chapter_result.get('content', '')[:150]}...")
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60 + "\n")
        
        if info['service'] == 'OpenRouter':
            print("⚠️  WARNING: Using OpenRouter fallback (rate limited)")
            print("   To use unlimited Custom LLM, add to .env:")
            print("   CLOUDFLARE_API_TOKEN=your_token")
            print("   CLOUDFLARE_ACCOUNT_ID=your_account_id")
            print("   Get them from: https://dash.cloudflare.com\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n💡 Quick Fix:")
        print("   1. Make sure .env has CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID")
        print("   2. Or ensure OPENROUTER_API_KEY is set for fallback")
        print("   3. Run: cd /home/badr/book-generator/backend")
        print("   4. Run: python test_integration.py\n")


if __name__ == '__main__':
    test_integration()
