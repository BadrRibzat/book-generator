from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import requests
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class GoogleFontsIntegration:
    """
    Google Fonts CSS2 API integration for dynamic font loading
    """
    
    FONT_CACHE_DIR = Path('/tmp/book_generator_fonts')
    
    def __init__(self):
        self.FONT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.loaded_fonts = set()
    
    def load_google_font(self, font_family: str, weight: int = 400) -> Optional[str]:
        """
        Load Google Font and return ReportLab-compatible font name
        
        Args:
            font_family: Google Font family name (e.g., 'Inter', 'Lato')
            weight: Font weight (400=normal, 700=bold)
            
        Returns:
            str: ReportLab font name or None if failed
        """
        font_name = f"{font_family.replace(' ', '')}-{weight}"
        
        if font_name in self.loaded_fonts:
            return font_name
        
        try:
            # Download font from Google Fonts API
            font_url = f"https://fonts.googleapis.com/css2?family={font_family.replace(' ', '+')}:wght@{weight}&display=swap"
            response = requests.get(font_url, timeout=10)
            response.raise_for_status()
            
            # Parse CSS to find .ttf URL
            css_content = response.text
            # Extract URL from @font-face src
            import re
            ttf_url_match = re.search(r'url\((https://[^)]+\.ttf)\)', css_content)
            
            if ttf_url_match:
                ttf_url = ttf_url_match.group(1)
                
                # Download .ttf file
                ttf_response = requests.get(ttf_url, timeout=15)
                ttf_response.raise_for_status()
                
                # Save to cache
                font_file = self.FONT_CACHE_DIR / f"{font_name}.ttf"
                font_file.write_bytes(ttf_response.content)
                
                # Register with ReportLab
                pdfmetrics.registerFont(TTFont(font_name, str(font_file)))
                
                self.loaded_fonts.add(font_name)
                logger.info(f"Loaded Google Font: {font_name}")
                
                return font_name
            else:
                logger.warning(f"Could not find TTF URL for {font_family}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to load Google Font {font_family}: {str(e)}")
            return None
    
    def get_fallback_font(self, category: str = 'clean_sans') -> str:
        """
        Get system fallback font based on category
        
        Args:
            category: Font category
            
        Returns:
            str: System font name
        """
        fallbacks = {
            'clean_sans': 'Helvetica',
            'elegant_serif': 'Times-Roman',
            'hand_written': 'Helvetica',
            'modern_geometric': 'Helvetica',
            'classic_traditional': 'Times-Roman'
        }
        return fallbacks.get(category, 'Helvetica')

class ProfessionalPDFGenerator:
    """
    Generate beautifully formatted PDFs with professional typography
    Supports dynamic font selection based on cover brief and domain
    """

    def __init__(self, font_theme=None):
        """
        Initialize PDF generator with optional font theme
        
        Args:
            font_theme: FontTheme model instance (optional)
        """
        self.font_theme = font_theme
        self.google_fonts = GoogleFontsIntegration()
        self.setup_fonts()
        self.setup_styles()

    def setup_fonts(self):
        """
        Register professional fonts dynamically based on font theme
        """
        if self.font_theme:
            # Load Google Fonts dynamically
            self.header_font = self.google_fonts.load_google_font(
                self.font_theme.header_font,
                self.font_theme.header_weight
            )
            self.body_font = self.google_fonts.load_google_font(
                self.font_theme.body_font,
                self.font_theme.body_weight
            )
            
            # Fallback to system fonts if Google Fonts failed
            if not self.header_font:
                self.header_font = self.google_fonts.get_fallback_font(self.font_theme.category)
            if not self.body_font:
                self.body_font = self.google_fonts.get_fallback_font(self.font_theme.category)
                
            logger.info(f"Using font theme: {self.font_theme.name} (Header: {self.header_font}, Body: {self.body_font})")
        else:
            # Default fonts (backward compatibility)
            self.header_font = 'Helvetica-Bold'
            self.body_font = 'Times-Roman'
            
            # Try to load system professional fonts
            font_paths = {
                'Montserrat-Bold': '/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf',
                'Lora-Regular': '/usr/share/fonts/truetype/lora/Lora-Regular.ttf',
            }

            for font_name, font_path in font_paths.items():
                try:
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                        if 'Bold' in font_name:
                            self.header_font = font_name
                        else:
                            self.body_font = font_name
                except Exception as e:
                    logger.warning(f"Could not load {font_name}: {e}")
    
    @classmethod
    def create_with_book_context(cls, book, cover_brief: str = None):
        """
        Create PDF generator with automatic font theme selection
        
        Args:
            book: Book model instance
            cover_brief: Optional cover brief for AI-based font selection
            
        Returns:
            ProfessionalPDFGenerator instance
        """
        try:
            from books.models import FontTheme
            
            if cover_brief:
                # Select font theme based on AI cover brief
                font_theme = FontTheme.select_font_theme_from_brief(cover_brief, book.domain)
            elif book.domain:
                # Select domain-specific font theme
                font_theme = FontTheme.objects.filter(
                    domain=book.domain,
                    is_active=True
                ).first()
            else:
                # Use default font theme
                font_theme = FontTheme.objects.filter(
                    is_default=True,
                    is_active=True
                ).first()
            
            return cls(font_theme=font_theme)
            
        except Exception as e:
            logger.error(f"Font theme selection failed: {str(e)}, using defaults")
            return cls()  # Fallback to default fonts

    def setup_styles(self):
        """
        Create professional paragraph styles with dynamic fonts
        """
        self.styles = getSampleStyleSheet()

        # Title Page Style
        self.styles.add(ParagraphStyle(
            name='BookTitle',
            parent=self.styles['Title'],
            fontSize=42,
            textColor=HexColor('#1a365d'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName=self.header_font,
            leading=50
        ))

        # Chapter Title Style
        self.styles.add(ParagraphStyle(
            name='ChapterTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=HexColor('#2c5282'),
            spaceAfter=20,
            spaceBefore=30,
            fontName=self.header_font,
            leading=34
        ))

        # Section Heading Style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=HexColor('#2d3748'),
            spaceAfter=12,
            spaceBefore=18,
            fontName=self.header_font,
            leading=22
        ))

        # Body Text Style - ENHANCED with dynamic font
        self.styles.add(ParagraphStyle(
            name='BookBody',
            parent=self.styles['BodyText'],
            fontSize=14,  # Increased from default 10-12
            textColor=HexColor('#2d3748'),
            spaceAfter=14,
            spaceBefore=0,
            alignment=TA_JUSTIFY,
            fontName=self.body_font,
            leading=21,  # 1.5 line spacing
            firstLineIndent=0
        ))

        # Bullet List Style
        self.styles.add(ParagraphStyle(
            name='BulletList',
            parent=self.styles['BookBody'],
            fontSize=14,
            leftIndent=25,
            bulletIndent=10,
            spaceAfter=10,
            leading=20
        ))

        # Quote Style
        self.styles.add(ParagraphStyle(
            name='Quote',
            parent=self.styles['BookBody'],
            fontSize=13,
            textColor=HexColor('#4a5568'),
            leftIndent=40,
            rightIndent=40,
            spaceAfter=16,
            spaceBefore=16,
            leading=19
        ))

    def create_book_pdf(self, book, content_data: Dict, output_path: str):
        """
        Create professionally formatted book PDF
        """
        # Create document with margins
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=1*inch,
            leftMargin=1*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )

        story = []

        # Title Page
        story.extend(self._create_title_page(book, content_data))
        story.append(PageBreak())

        # Table of Contents
        story.extend(self._create_toc(content_data))
        story.append(PageBreak())

        # Introduction
        if 'introduction' in content_data:
            story.extend(self._format_chapter('Introduction', content_data['introduction']))
            story.append(PageBreak())

        # Main Chapters
        for chapter in content_data.get('chapters', []):
            story.extend(self._format_chapter(chapter['title'], chapter['content']))
            story.append(PageBreak())

        # Conclusion
        if 'conclusion' in content_data:
            story.extend(self._format_chapter('Conclusion', content_data['conclusion']))
            story.append(PageBreak())

        # Actionable Takeaways
        if 'takeaways' in content_data:
            story.extend(self._format_chapter('Actionable Takeaways', content_data['takeaways']))

        # Build PDF
        doc.build(story)

        return output_path

    def _create_title_page(self, book, content_data: Dict) -> List:
        """Create professional title page"""
        elements = []

        # Add spacer for vertical centering
        elements.append(Spacer(1, 2*inch))

        # Book Title
        title = Paragraph(book.title, self.styles['BookTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))

        # Subtitle (if exists)
        if 'subtitle' in content_data:
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=self.styles['BookBody'],
                fontSize=16,
                textColor=HexColor('#4a5568'),
                alignment=TA_CENTER,
                spaceAfter=30
            )
            elements.append(Paragraph(content_data['subtitle'], subtitle_style))

        # Domain/Category
        domain_style = ParagraphStyle(
            'Domain',
            parent=self.styles['BookBody'],
            fontSize=12,
            textColor=HexColor('#718096'),
            alignment=TA_CENTER,
            spaceAfter=10
        )
        elements.append(Paragraph(f"<b>{book.domain.name}</b>", domain_style))

        return elements

    def _format_chapter(self, title: str, content: str) -> List:
        """Format chapter with professional styling"""
        elements = []

        # Chapter Title
        elements.append(Paragraph(title, self.styles['ChapterTitle']))
        elements.append(Spacer(1, 0.3*inch))

        # Split content into sections and paragraphs
        sections = content.split('####')

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Check if section has a heading
            lines = section.split('\n', 1)
            if len(lines) > 1 and lines[0].strip():
                # Section heading
                heading = lines[0].strip()
                section_content = lines[1].strip()

                elements.append(Paragraph(heading, self.styles['SectionHeading']))
                elements.append(Spacer(1, 0.15*inch))
            else:
                section_content = section

            # Process paragraphs
            paragraphs = [p.strip() for p in section_content.split('\n') if p.strip()]

            for para in paragraphs:
                # Handle bullet points
                if para.startswith('- '):
                    bullet_items = [item.strip('- ').strip() for item in para.split('\n- ')]
                    for item in bullet_items:
                        elements.append(Paragraph(f'• {item}', self.styles['BulletList']))
                else:
                    # Regular paragraph
                    # Ensure minimum length - pad if necessary
                    if len(para.split()) < 30:
                        # Skip very short paragraphs that might be artifacts
                        if len(para.split()) > 5:
                            elements.append(Paragraph(para, self.styles['BookBody']))
                    else:
                        elements.append(Paragraph(para, self.styles['BookBody']))

                elements.append(Spacer(1, 0.12*inch))

        return elements

    def _create_toc(self, content_data: Dict) -> List:
        """Create table of contents"""
        elements = []

        toc_title = Paragraph('Table of Contents', self.styles['ChapterTitle'])
        elements.append(toc_title)
        elements.append(Spacer(1, 0.3*inch))

        toc_style = ParagraphStyle(
            'TOCEntry',
            parent=self.styles['BookBody'],
            fontSize=13,
            spaceAfter=8,
            leftIndent=20
        )

        # Add TOC entries
        toc_entries = []
        toc_entries.append('Introduction')

        for i, chapter in enumerate(content_data.get('chapters', []), 1):
            toc_entries.append(f'Chapter {i}: {chapter["title"]}')

        toc_entries.append('Conclusion')
        toc_entries.append('Actionable Takeaways')

        for entry in toc_entries:
            elements.append(Paragraph(f'• {entry}', toc_style))

        return elements