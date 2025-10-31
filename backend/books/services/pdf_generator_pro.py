from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, PageBreak,
    Frame, PageTemplate
)
from reportlab.platypus.tableofcontents import TableOfContents
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
        self.typography_scale = self._build_typography_scale()
        self.brand_palette = self._build_brand_palette()
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

        if not self._font_available(self.header_font):
            self.header_font = 'Helvetica-Bold'
        if not self._font_available(self.body_font):
            self.body_font = 'Helvetica'

    def _build_typography_scale(self) -> Dict[str, int]:
        """Define a consistent typographic scale used throughout the book."""
        return {
            'display': 44,
            'headline': 28,
            'subhead': 18,
            'body': 14,
            'small': 10,
        }

    def _build_brand_palette(self) -> Dict[str, HexColor]:
        """Centralise brand colors for headers, footers, and accents."""
        return {
            'primary': HexColor('#1E3A8A'),
            'accent': HexColor('#F97316'),
            'light': HexColor('#F8FAFC'),
            'muted': HexColor('#475569'),
        }

    def _font_available(self, font_name: str) -> bool:
        try:
            pdfmetrics.getFont(font_name)
            return True
        except KeyError:
            return False
    
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
            fontSize=self.typography_scale['display'],
            textColor=HexColor('#1a365d'),
            spaceAfter=self.typography_scale['body'] * 2,
            alignment=TA_CENTER,
            fontName=self.header_font,
            leading=int(self.typography_scale['display'] * 1.2)
        ))

        # Chapter Title Style
        self.styles.add(ParagraphStyle(
            name='ChapterTitle',
            parent=self.styles['Heading1'],
            fontSize=self.typography_scale['headline'],
            textColor=HexColor('#2c5282'),
            spaceAfter=self.typography_scale['body'],
            spaceBefore=self.typography_scale['body'] * 2,
            fontName=self.header_font,
            leading=int(self.typography_scale['headline'] * 1.2)
        ))

        # Section Heading Style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=self.typography_scale['subhead'],
            textColor=HexColor('#2d3748'),
            spaceAfter=self.typography_scale['body'] * 0.8,
            spaceBefore=self.typography_scale['body'],
            fontName=self.header_font,
            leading=int(self.typography_scale['subhead'] * 1.2)
        ))

        # Body Text Style - ENHANCED with dynamic font
        self.styles.add(ParagraphStyle(
            name='BookBody',
            parent=self.styles['BodyText'],
            fontSize=self.typography_scale['body'],
            textColor=HexColor('#2d3748'),
            spaceAfter=self.typography_scale['body'] * 0.9,
            spaceBefore=0,
            alignment=TA_JUSTIFY,
            fontName=self.body_font,
            leading=int(self.typography_scale['body'] * 1.5),
            firstLineIndent=0
        ))

        # Bullet List Style
        self.styles.add(ParagraphStyle(
            name='BulletList',
            parent=self.styles['BookBody'],
            fontSize=self.typography_scale['body'],
            leftIndent=25,
            bulletIndent=10,
            spaceAfter=self.typography_scale['body'] * 0.7,
            leading=int(self.typography_scale['body'] * 1.35)
        ))

        # Quote Style
        self.styles.add(ParagraphStyle(
            name='Quote',
            parent=self.styles['BookBody'],
            fontSize=max(self.typography_scale['body'] - 1, 12),
            textColor=HexColor('#4a5568'),
            leftIndent=40,
            rightIndent=40,
            spaceAfter=self.typography_scale['body'],
            spaceBefore=self.typography_scale['body'],
            leading=int(self.typography_scale['body'] * 1.4)
        ))

    def create_book_pdf(self, book, content_data: Dict, output_path: str):
        """
        Create professionally formatted book PDF
        """
        self._active_book_title = book.title

        # KDP-ready 6x9 inches with professional margins and headers
        SIX_BY_NINE = (6*inch, 9*inch)
        # Mirrored margins with gutter: inner margin a bit larger than outer
        inner_margin = 0.875*inch
        outer_margin = 0.625*inch
        top_margin = 0.75*inch
        bottom_margin = 0.75*inch

        # Custom DocTemplate to collect TOC entries
        class ProfessionalDocTemplate(BaseDocTemplate):
            def afterFlowable(self, flowable):
                try:
                    # Register headings for TOC
                    if isinstance(flowable, Paragraph):
                        style_name = flowable.style.name
                        # Only include chapters in TOC (not subsections) for a cleaner TOC
                        if style_name == 'ChapterTitle':
                            level = 0
                            text = flowable.getPlainText()
                            # Notify for TOC collection
                            self.notify('TOCEntry', (level, text, self.page))
                            self._current_chapter_title = text
                except Exception:
                    pass

        # Use DocTemplate with mirrored frames
        doc = ProfessionalDocTemplate(
            output_path,
            pagesize=SIX_BY_NINE,
            topMargin=top_margin,
            bottomMargin=bottom_margin,
        )

        page_width, page_height = SIX_BY_NINE

        # Right-hand (odd) pages: inner margin on the left
        right_frame = Frame(
            x1=inner_margin,
            y1=bottom_margin,
            width=page_width - inner_margin - outer_margin,
            height=page_height - top_margin - bottom_margin,
            id='right_frame'
        )

        # Left-hand (even) pages: inner margin on the right
        left_frame = Frame(
            x1=outer_margin,
            y1=bottom_margin,
            width=page_width - inner_margin - outer_margin,
            height=page_height - top_margin - bottom_margin,
            id='left_frame'
        )

        def _header_footer(canvas_obj, doc_obj, generator=self):
            generator._render_page_signature(
                canvas_obj,
                doc_obj,
                page_size=SIX_BY_NINE,
                margins=(inner_margin, outer_margin, top_margin, bottom_margin),
            )

        # Two page templates to mirror margins
        right_template = PageTemplate(id='Right', frames=[right_frame], onPage=_header_footer)
        left_template = PageTemplate(id='Left', frames=[left_frame], onPage=_header_footer)
        doc.addPageTemplates([right_template, left_template])
        doc._current_chapter_title = book.title

        story = []

        # Title Page
        story.extend(self._create_title_page(book, content_data))
        story.append(PageBreak())

        # Table of Contents (auto-generated with page numbers)
        toc_title = Paragraph('Table of Contents', self.styles['ChapterTitle'])
        story.append(toc_title)
        story.append(Spacer(1, 0.3*inch))
        toc = TableOfContents()
        # TOC level styles
        toc.levelStyles = [
            ParagraphStyle(
                name='TOCLevel0', parent=self.styles['BookBody'], fontSize=12, leftIndent=10, firstLineIndent=-10, spaceAfter=6
            ),
            ParagraphStyle(
                name='TOCLevel1', parent=self.styles['BookBody'], fontSize=11, leftIndent=30, firstLineIndent=-10, spaceAfter=4
            ),
        ]
        story.append(toc)
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

        # Build PDF with TOC resolution (multi-pass)
        doc.multiBuild(story)

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
        # Decorative divider under chapter title
        from reportlab.platypus import Flowable
        class HR(Flowable):
            def __init__(self, width=1, color=HexColor('#CBD5E0')):
                Flowable.__init__(self)
                self.width = width
                self.color = color
            def draw(self):
                self.canv.setStrokeColor(self.color)
                self.canv.setLineWidth(self.width)
                self.canv.line(0, 0, self.canv._pagesize[0] - 2*0.75*inch, 0)
        elements.append(Spacer(1, 0.1*inch))
        elements.append(HR(width=1))
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

    def _render_page_signature(self, canvas_obj, doc_obj, page_size, margins):
        """Draw brand header, footer, and navigation markers per page."""
        canvas_obj.saveState()
        width, height = page_size
        inner_margin, outer_margin, top_margin, bottom_margin = margins
        on_left_page = (doc_obj.page % 2 == 0)

        chapter_title = getattr(doc_obj, '_current_chapter_title', self._active_book_title)
        chapter_label = (chapter_title or self._active_book_title or '').strip()
        chapter_label = chapter_label[:70]

        header_y = height - top_margin + 16
        logo_size = 0.52 * inch
        self._draw_brand_logo(canvas_obj, width / 2, header_y, logo_size)

        if chapter_label:
            canvas_obj.setFont(self.body_font, self.typography_scale['small'])
            canvas_obj.setFillColor(self.brand_palette['muted'])
            if on_left_page:
                canvas_obj.drawRightString(width - outer_margin, header_y - 6, chapter_label)
            else:
                canvas_obj.drawString(inner_margin, header_y - 6, chapter_label)

        strap_height = 0.22 * inch
        strap_y = bottom_margin - strap_height - 6
        canvas_obj.setFillColor(self.brand_palette['primary'])
        canvas_obj.rect(0, strap_y, width, strap_height, stroke=0, fill=1)

        footer_y = strap_y + strap_height / 2 - 3
        canvas_obj.setFont(self.body_font, self.typography_scale['small'])
        canvas_obj.setFillColor(self.brand_palette['light'])
        canvas_obj.drawString(inner_margin, footer_y, "BookAI Platform")
        canvas_obj.drawCentredString(width / 2, footer_y, f"Page {doc_obj.page}")
        if chapter_label:
            canvas_obj.drawRightString(width - inner_margin, footer_y, chapter_label)

        canvas_obj.restoreState()

    def _draw_brand_logo(self, canvas_obj, center_x: float, center_y: float, width: float):
        """Render a simplified brand mark derived from the frontend logo."""
        book_width = width
        book_height = width * 0.62
        left_x = center_x - book_width / 2
        bottom_y = center_y - book_height / 2

        canvas_obj.setFillColor(self.brand_palette['primary'])
        canvas_obj.roundRect(left_x, bottom_y, book_width, book_height, width * 0.12, stroke=0, fill=1)

        spine_width = width * 0.12
        canvas_obj.setFillColor(self.brand_palette['light'])
        canvas_obj.rect(center_x - spine_width / 2, bottom_y + book_height * 0.12, spine_width, book_height * 0.76, stroke=0, fill=1)

        accent_width = width * 0.28
        canvas_obj.setFillColor(self.brand_palette['accent'])
        canvas_obj.roundRect(left_x + book_width - accent_width, bottom_y + book_height * 0.08, accent_width, book_height * 0.84, width * 0.1, stroke=0, fill=1)

        canvas_obj.setFillColor(self.brand_palette['light'])
        canvas_obj.setFont(self.header_font, max(10, int(book_height * 0.85)))
        canvas_obj.drawCentredString(center_x, center_y - book_height * 0.18, "AI")

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