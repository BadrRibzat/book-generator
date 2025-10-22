#!/usr/bin/env python
"""
Simple test for cover generation fix
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, '/home/badr/book-generator/backend')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from covers.services import CoverGenerator

def test_cover_generator():
    """Test the CoverGenerator class"""
    print("Testing CoverGenerator...")

    # Create a mock book object
    class MockBook:
        def __init__(self):
            self.id = 999
            self.title = "Test Book Title"
            self.sub_niche = "ai_productivity_tools"

    book = MockBook()
    generator = CoverGenerator()

    # Test the _get_modern_css method
    try:
        css = generator._get_modern_css()
        print("✓ _get_modern_css method exists and returns CSS")
        print(f"  CSS length: {len(css)} characters")
    except AttributeError as e:
        print(f"✗ _get_modern_css method missing: {e}")
        return False
    except Exception as e:
        print(f"✗ Error calling _get_modern_css: {e}")
        return False

    # Test generating AI concepts
    try:
        concepts = generator._generate_ai_cover_concepts(book)
        print(f"✓ AI concepts generated: {len(concepts)} concepts")
        for i, concept in enumerate(concepts):
            print(f"  Concept {i+1}: {concept.get('trend', 'unknown')} - {concept.get('title', 'no title')}")
    except Exception as e:
        print(f"✗ Error generating AI concepts: {e}")
        return False

    print("✓ All tests passed!")
    return True

if __name__ == "__main__":
    success = test_cover_generator()
    sys.exit(0 if success else 1)