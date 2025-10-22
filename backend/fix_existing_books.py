#!/usr/bin/env python
"""
Fix existing books that don't have chapters parsed
This updates MongoDB documents to add the 'chapters' key
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.services.book_generator import BookGeneratorProfessional
from books.models import Book
from backend.utils.mongodb import get_mongodb_db
from bson import ObjectId

def fix_existing_books():
    """Fix all existing books without chapters"""
    db = get_mongodb_db()
    generator = BookGeneratorProfessional()
    
    # Find all book contents without chapters key
    cursor = db.book_contents.find({'$or': [
        {'content.chapters': {'$exists': False}},
        {'content.chapters': []}
    ]})
    
    fixed_count = 0
    
    for doc in cursor:
        book_id = doc.get('book_id')
        content_data = doc.get('content', {})
        
        if not isinstance(content_data, dict):
            print(f"⚠ Skipping book {book_id}: content is not a dict")
            continue
        
        # Check if chapters exist
        if 'chapters' in content_data and len(content_data['chapters']) > 0:
            print(f"✓ Book {book_id}: already has chapters")
            continue
        
        # Get the raw content
        raw_content = content_data.get('content', '')
        if not raw_content or not isinstance(raw_content, str):
            print(f"⚠ Skipping book {book_id}: no raw content")
            continue
        
        # Get the book object to get page_length
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            print(f"⚠ Skipping: Book {book_id} not found in database")
            continue
        
        print(f"\nFixing book {book_id}: {book.title}")
        print(f"  Current title in DB: {book.title}")
        
        # Parse content into chapters
        parsed = generator.parse_book_content(raw_content, book.page_length)
        chapters = parsed.get('chapters', [])
        
        if len(chapters) == 0:
            print(f"  ⚠ Warning: No chapters could be parsed")
            continue
        
        print(f"  ✓ Parsed {len(chapters)} chapters")
        
        # Extract title again in case it's still "Generating..."
        if book.title == "Generating...":
            title = generator.extract_title(raw_content)
            if title:
                print(f"  ✓ Extracted title: {title}")
                book.title = title
                book.save()
                content_data['title'] = title
        
        # Update content_data with chapters
        content_data['chapters'] = chapters
        
        # Update MongoDB
        result = db.book_contents.update_one(
            {'_id': doc['_id']},
            {'$set': {'content': content_data}}
        )
        
        if result.modified_count > 0:
            print(f"  ✓ Updated MongoDB for book {book_id}")
            fixed_count += 1
            
            # Regenerate interior PDF if needed
            interior_path = doc.get('interior_pdf_path')
            if interior_path:
                from pathlib import Path
                if not Path(interior_path).exists() or Path(interior_path).stat().st_size < 10000:
                    print(f"  ℹ Regenerating interior PDF (old was {Path(interior_path).stat().st_size if Path(interior_path).exists() else 0} bytes)...")
                    try:
                        new_interior_path = generator.create_pdf(book, content_data)
                        db.book_contents.update_one(
                            {'_id': doc['_id']},
                            {'$set': {'interior_pdf_path': new_interior_path}}
                        )
                        print(f"  ✓ Regenerated interior PDF: {new_interior_path}")
                    except Exception as e:
                        print(f"  ✗ Failed to regenerate PDF: {e}")
        else:
            print(f"  ✗ Failed to update MongoDB for book {book_id}")
    
    print(f"\n{'='*60}")
    print(f"Fixed {fixed_count} books")
    print(f"{'='*60}")

if __name__ == '__main__':
    print("=" * 60)
    print("FIXING EXISTING BOOKS")
    print("=" * 60)
    print()
    
    try:
        fix_existing_books()
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
