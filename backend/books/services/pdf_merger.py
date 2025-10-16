# books/services/pdf_merger.py
import os
from pathlib import Path
from pypdf import PdfWriter, PdfReader
from django.conf import settings
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4

class PDFMerger:
    """
    Merges cover PDF with interior content PDF
    Creates final downloadable book
    """
    
    def __init__(self):
        self.media_root = Path(settings.MEDIA_ROOT)
        self.books_dir = self.media_root / 'books'
        self.books_dir.mkdir(parents=True, exist_ok=True)
    
    def merge_book(self, book, interior_pdf_path, cover):
        """
        Merge cover + interior into final book PDF
        
        Args:
            book: Book model instance
            interior_pdf_path: Path to generated interior PDF
            cover: Cover model instance
            
        Returns:
            Path to final merged PDF
        """
        output_filename = f"book_{book.id}_final.pdf"
        output_path = self.books_dir / output_filename
        
        writer = PdfWriter()
        
        # Add cover as first page
        cover_pdf_path = self.media_root / cover.pdf_path
        if cover_pdf_path.exists():
            cover_reader = PdfReader(str(cover_pdf_path))
            writer.add_page(cover_reader.pages[0])
        
        # Add interior pages
        if os.path.exists(interior_pdf_path):
            interior_reader = PdfReader(interior_pdf_path)
            for page in interior_reader.pages:
                writer.add_page(page)
        
        # Write merged PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return f"books/{output_filename}"
