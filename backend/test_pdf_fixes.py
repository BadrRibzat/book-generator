#!/usr/bin/env python
"""
Test script to verify PDF generation fixes
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Django imports
from books.models import Book
from books.services.pdf_merger import PDFMerger
from covers.models import Cover
from covers.services import CoverGenerator

def test_cover_generator():
    """Test CoverGenerator HTML to PDF conversion"""
    print("Testing CoverGenerator...")
    
    # Get an existing book or create a test one
    books = Book.objects.filter(status='ready')
    
    if books.exists():
        book = books.first()
        print(f"Using existing book: {book.id} - {book.title}")
    else:
        # Create test user
        from django.contrib.auth.models import User
        test_user, created = User.objects.get_or_create(
            username="test_pdf_user", 
            defaults={"email": "test@example.com"}
        )
        if created:
            test_user.set_password("testpassword123")
            test_user.save()
            print(f"Created test user: {test_user.username}")
        else:
            print(f"Using existing user: {test_user.username}")
        
        book = Book.objects.create(
            title="Test PDF Generation Book",
            status="ready",
            page_length=15,
            domain="technology",
            sub_niche="ai_ethics",
            user=test_user
        )
        print(f"Created test book: {book.id} - {book.title}")
    
    # Generate covers
    try:
        print("Generating test covers...")
        cover_gen = CoverGenerator()
        covers = cover_gen.generate_three_covers(book)
        
        print(f"Successfully generated {len(covers)} covers")
        for i, cover in enumerate(covers):
            print(f"  Cover {i+1}: {cover.template_style} (PDF: {cover.pdf_path})")
        
        return covers
    except Exception as e:
        print(f"ERROR: Cover generation failed: {str(e)}")
        return []

def test_pdf_merger(book, covers):
    """Test PDFMerger with the generated covers"""
    if not covers:
        print("No covers available for PDF merger test")
        return False
    
    print("\nTesting PDFMerger...")
    
    # Create a dummy interior PDF
    from reportlab.pdfgen import canvas
    test_pdf_path = "test_interior.pdf"
    c = canvas.Canvas(test_pdf_path)
    c.drawString(100, 750, "Test Interior PDF")
    c.showPage()  # Add a page
    c.save()
    
    print(f"Created test interior PDF: {test_pdf_path}")
    
    # Test merger with each cover
    results = []
    for i, cover in enumerate(covers):
        try:
            print(f"\nTrying merger with cover {i+1}: {cover.template_style}")
            merger = PDFMerger()
            output_path = merger.merge_book(book, test_pdf_path, cover)
            
            print(f"  Success! Merged PDF saved to: {output_path}")
            results.append((True, output_path))
        except Exception as e:
            print(f"  ERROR: PDF merger failed: {str(e)}")
            results.append((False, str(e)))
    
    # Clean up
    if os.path.exists(test_pdf_path):
        os.remove(test_pdf_path)
    
    # Report results
    success_count = sum(1 for r in results if r[0])
    print(f"\nPDF merger results: {success_count}/{len(results)} successful")
    
    return success_count > 0

def main():
    """Run all tests"""
    print("="*70)
    print("PDF GENERATION FIX VERIFICATION")
    print("="*70)
    
    # Test cover generation
    covers = test_cover_generator()
    
    if not covers:
        print("\n❌ Cover generation test failed")
        return False
    
    print("\n✅ Cover generation test passed")
    
    # Get a book for testing
    book = covers[0].book
    
    # Test PDF merger
    merger_success = test_pdf_merger(book, covers)
    
    if not merger_success:
        print("\n❌ PDF merger test failed")
        return False
    
    print("\n✅ PDF merger test passed")
    
    # Overall success
    print("\n" + "="*70)
    print("✅ ALL PDF GENERATION TESTS PASSED!")
    print("="*70)
    print("\nThe PDF generation fixes have been verified successfully.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)