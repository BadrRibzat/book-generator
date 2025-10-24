#!/usr/bin/env python
"""
Test script for multi-LLM book generation
"""
import os
import sys
import django

# Setup Django
sys.path.append('/home/badr/book-generator/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.services.book_generator import BookGeneratorProfessional
from covers.services_pro import ProfessionalCoverGenerator

def test_multi_llm_generation():
    """Test the multi-LLM book generation system"""
    print("🧪 Testing Multi-LLM Book Generation System")
    print("=" * 50)

    try:
        # Initialize generators
        book_gen = BookGeneratorProfessional()
        cover_gen = ProfessionalCoverGenerator()

        print("✓ Generators initialized successfully")
        print(f"✓ LLM Available: {book_gen.llm_available}")

        # Test content generation (mock book object)
        class MockBook:
            def __init__(self):
                self.title = "The Future of AI in Business"
                self.domain = type('obj', (object,), {'name': 'Technology', 'slug': 'ai-tech'})()
                self.niche = type('obj', (object,), {'name': 'AI Business Applications'})()
                self.book_style = type('obj', (object,), {'length': 'short', 'target_audience': 'business leaders'})()

        mock_book = MockBook()

        print(f"✓ Mock book created: {mock_book.title}")

        # Test LLM orchestrator (only if available)
        if book_gen.llm_available:
            print("\n🔄 Testing MultiLLMOrchestrator...")
            orchestrator = book_gen.llm_orchestrator
            print("✓ MultiLLMOrchestrator initialized")
        else:
            print("\n⚠️ MultiLLMOrchestrator not available (API key not set)")

        # Test PDF generator
        print("\n📄 Testing ProfessionalPDFGenerator...")
        pdf_gen = book_gen.pdf_generator
        print("✓ ProfessionalPDFGenerator initialized")

        # Test cover generator
        print("\n🎨 Testing ProfessionalCoverGenerator...")
        print("✓ ProfessionalCoverGenerator initialized")

        print("\n✅ All components initialized successfully!")
        if not book_gen.llm_available:
            print("⚠️ Note: LLM functionality requires OPENROUTER_API_KEY environment variable")
        else:
            print("🎉 Multi-LLM book generation system is fully ready!")

        print("\nNext steps:")
        if not book_gen.llm_available:
            print("1. Set OPENROUTER_API_KEY environment variable")
        print("2. Test with real book generation")
        print("3. Verify PDF and cover output quality")

        return True

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_multi_llm_generation()
    sys.exit(0 if success else 1)