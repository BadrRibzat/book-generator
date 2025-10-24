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
from pathlib import Path
from typing import Dict, List

class ProfessionalPDFGenerator:
    """
    Generate beautifully formatted PDFs with professional typography
    """

    def __init__(self):
        self.setup_fonts()
        self.setup_styles()

    def setup_fonts(self):
        """
        Register professional fonts (using system fonts or download free ones)
        """
        # Try to register common professional fonts
        font_paths = {
            'Montserrat-Bold': '/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf',
            'Montserrat-Regular': '/usr/share/fonts/truetype/montserrat/Montserrat-Regular.ttf',
            'Lora-Regular': '/usr/share/fonts/truetype/lora/Lora-Regular.ttf',
            'Lora-Bold': '/usr/share/fonts/truetype/lora/Lora-Bold.ttf',
        }

        for font_name, font_path in font_paths.items():
            try:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
            except Exception as e:
                print(f"Could not load {font_name}: {e}")

    def setup_styles(self):
        """
        Create professional paragraph styles
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
            fontName='Montserrat-Bold' if 'Montserrat-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
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
            fontName='Montserrat-Bold' if 'Montserrat-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
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
            fontName='Montserrat-Bold' if 'Montserrat-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold',
            leading=22
        ))

        # Body Text Style - ENHANCED
        self.styles.add(ParagraphStyle(
            name='BookBody',
            parent=self.styles['BodyText'],
            fontSize=14,  # Increased from default 10-12
            textColor=HexColor('#2d3748'),
            spaceAfter=14,
            spaceBefore=0,
            alignment=TA_JUSTIFY,
            fontName='Lora-Regular' if 'Lora-Regular' in pdfmetrics.getRegisteredFontNames() else 'Times-Roman',
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