# books/services/pdf_merger.py
import os
from pathlib import Path
from pypdf import PdfWriter, PdfReader
from django.conf import settings
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class PDFMerger:
    """
    Creates final book PDF by generating cover with ReportLab and merging with interior
    """
    
    def __init__(self):
        self.media_root = Path(settings.MEDIA_ROOT)
        self.books_dir = self.media_root / 'books'
        self.covers_dir = self.media_root / 'covers'
        self.books_dir.mkdir(parents=True, exist_ok=True)
        self.covers_dir.mkdir(parents=True, exist_ok=True)
    
    def merge_book(self, book, interior_pdf_path, cover):
        """
        Generate cover with ReportLab and merge with interior into final book PDF
        
        Args:
            book: Book model instance
            interior_pdf_path: Path to generated interior PDF
            cover: Cover model instance with generation_params
            
        Returns:
            Path to final merged PDF
        """
        # Use clean book title for filename
        clean_title = self._clean_filename(book.title)
        output_filename = f"{clean_title}.pdf"
        output_path = self.books_dir / output_filename
        
        writer = PdfWriter()
        
        # Generate cover PDF using ReportLab
        cover_pdf_buffer = self._generate_cover_pdf(book, cover)
        if cover_pdf_buffer:
            cover_reader = PdfReader(cover_pdf_buffer)
            if len(cover_reader.pages) > 0:
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
    
    def _generate_cover_pdf(self, book, cover):
        """
        Generate cover PDF using ReportLab based on cover generation params
        
        Args:
            book: Book model instance
            cover: Cover model instance
            
        Returns:
            BytesIO buffer containing PDF data
        """
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Get cover parameters
        gen_params = cover.generation_params or {}
        colors = gen_params.get('colors', {})
        mood = gen_params.get('mood', 'professional')
        trend = gen_params.get('trend_style', 'modern')
        
        # Set up background based on trend
        self._draw_cover_background(c, trend, colors)
        
        # Draw title
        self._draw_cover_title(c, book.title, trend, colors)
        
        # Add decorative elements based on trend
        self._draw_cover_elements(c, trend, colors)
        
        c.save()
        buffer.seek(0)
        return buffer
    
    def _draw_cover_background(self, c, trend, colors):
        """Draw background based on design trend"""
        width, height = letter
        
        if 'glass' in trend.lower():
            # Glassmorphism effect
            c.setFillColor(HexColor(colors.get('background', '#f8fafc')))
            c.rect(0, 0, width, height, fill=1)
            
            # Frosted glass overlay
            c.setFillColor(HexColor(colors.get('primary', '#3b82f6') + '40'))  # 25% opacity
            c.roundRect(1*inch, 1*inch, width-2*inch, height-2*inch, 24, fill=1)
            
        elif 'neo' in trend.lower():
            # Neomorphism
            c.setFillColor(HexColor(colors.get('background', '#f1f5f9')))
            c.rect(0, 0, width, height, fill=1)
            
            # Soft shadow effect
            c.setFillColor(HexColor(colors.get('primary', '#2d3748') + '20'))  # Light shadow
            c.roundRect(2*inch, 2*inch, width-4*inch, height-4*inch, 40, fill=1)
            
        elif 'brutal' in trend.lower():
            # Brutalist
            c.setFillColor(HexColor(colors.get('primary', '#000000')))
            c.rect(0, 0, width, height, fill=1)
            
            # White content area with border
            c.setFillColor(HexColor(colors.get('background', '#ffffff')))
            c.rect(0.5*inch, 0.5*inch, width-1*inch, height-1*inch, fill=1)
            c.setStrokeColor(HexColor(colors.get('primary', '#000000')))
            c.setLineWidth(10)
            c.rect(0.5*inch, 0.5*inch, width-1*inch, height-1*inch, fill=0)
            
        else:  # minimalist or default
            # Clean background
            c.setFillColor(HexColor(colors.get('background', '#ffffff')))
            c.rect(0, 0, width, height, fill=1)
            
            # Subtle geometric element
            c.setFillColor(HexColor(colors.get('primary', '#3b82f6') + '15'))  # 10% opacity
            c.rect(width-4*inch, height-4*inch, 3*inch, 3*inch, fill=1)
    
    def _draw_cover_title(self, c, title, trend, colors):
        """Draw the book title on the cover"""
        width, height = letter
        
        # Split title for better layout
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        
        # Set font and color based on trend
        if 'brutal' in trend.lower():
            c.setFillColor(HexColor(colors.get('primary', '#000000')))
            c.setFont("Helvetica-Bold", 56)
            c.drawCentredString(width/2, height/2 + 1*inch, title_line1)
            if title_line2:
                c.setFont("Helvetica-Bold", 40)
                c.drawCentredString(width/2, height/2 + 0.5*inch, title_line2)
        elif 'cyber' in trend.lower():
            c.setFillColor(HexColor(colors.get('accent', '#ec4899')))
            c.setFont("Helvetica-Bold", 48)
            # Add glow effect by drawing multiple times
            for offset in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)]:
                if offset == (0, 0):
                    c.setFillColor(HexColor(colors.get('accent', '#ec4899')))
                else:
                    c.setFillColor(HexColor(colors.get('accent', '#ec4899') + '40'))
                c.drawCentredString(width/2 + offset[0], height/2 + 1*inch + offset[1], title_line1)
            if title_line2:
                c.setFont("Helvetica-Bold", 32)
                c.drawCentredString(width/2, height/2 + 0.5*inch, title_line2)
        else:  # default professional
            c.setFillColor(HexColor(colors.get('primary', '#1a365d')))
            c.setFont("Helvetica-Bold", 48)
            c.drawCentredString(width/2, height/2 + 1*inch, title_line1)
            if title_line2:
                c.setFont("Helvetica-Bold", 32)
                c.drawCentredString(width/2, height/2 + 0.5*inch, title_line2)
    
    def _draw_cover_elements(self, c, trend, colors):
        """Draw decorative elements based on trend"""
        width, height = letter
        
        if 'organic' in trend.lower():
            # Organic shapes
            c.setFillColor(HexColor(colors.get('accent', '#10b981') + '30'))
            # Draw irregular blob shape
            c.roundRect(1*inch, 1*inch, 3*inch, 3*inch, 60, fill=1)
            
        elif 'cyber' in trend.lower():
            # Grid pattern
            c.setStrokeColor(HexColor(colors.get('secondary', '#8b5cf6') + '40'))
            c.setLineWidth(1)
            for x in range(0, int(width), 60):
                c.line(x, 0, x, height)
            for y in range(0, int(height), 60):
                c.line(0, y, width, y)
                
        elif 'minimalist' in trend.lower():
            # Simple accent line
            c.setStrokeColor(HexColor(colors.get('accent', '#3b82f6')))
            c.setLineWidth(4)
            c.line(2*inch, 2*inch, width-2*inch, 2*inch)
    
    def _clean_filename(self, title: str) -> str:
        """Clean book title for filename"""
        # Remove special characters, keep alphanumeric, spaces, hyphens, underscores
        cleaned = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
        # Truncate if too long
        cleaned = cleaned[:100]
        # Replace spaces with underscores
        cleaned = '_'.join(cleaned.split())
        return cleaned or "Professional_Book"
