#!/usr/bin/env python
"""
Regenerate final PDF for book 43 with correct title
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.models import Book
from books.services.pdf_merger import PDFMerger
from backend.utils.mongodb import get_mongodb_db

# Get book 43
book = Book.objects.get(id=43)
print(f'Book: {book.title}')
print(f'Status: {book.status}')
print(f'Selected cover: {book.selected_cover}')

# Get interior PDF path from MongoDB  
db = get_mongodb_db()
content_doc = db.book_contents.find_one({'book_id': 43})
interior_pdf_path = content_doc.get('interior_pdf_path')

print(f'Interior PDF: {interior_pdf_path}')

if book.selected_cover and interior_pdf_path:
    # Merge with selected cover
    merger = PDFMerger()
    final_pdf_path = merger.merge_book(
        book,
        interior_pdf_path,
        book.selected_cover
    )
    
    # Update MongoDB
    db.book_contents.update_one(
        {'book_id': 43},
        {'$set': {'final_pdf_path': final_pdf_path}}
    )
    
    print(f'\n✓ Final PDF created: {final_pdf_path}')
    print(f'✓ MongoDB updated')
else:
    print('⚠ Missing cover or interior PDF')
