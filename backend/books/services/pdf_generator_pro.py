from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Paragraph, Spacer, PageBreak,
    Frame, PageTemplate, NextPageTemplate, HRFlowable, Preformatted
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
import logging
import re
from typing import Dict, List, Optional, Tuple

from backend.utils.fonts import GoogleFontsIntegration
from covers.template_library import get_domain_typography

logger = logging.getLogger(__name__)
class ProfessionalPDFGenerator:
    """
    Generate beautifully formatted PDFs with professional typography
    Supports dynamic font selection based on cover brief and domain
    """

    def __init__(self, font_theme=None, domain_slug: str = ""):
        """
        Initialize PDF generator with optional font theme

        Args:
            font_theme: FontTheme model instance (optional)
            domain_slug: Domain slug used for typography mapping
        """
        self.font_theme = font_theme
        self.domain_slug = (domain_slug or "").strip().lower()
        self.domain_typography = get_domain_typography(self.domain_slug)
        self.accent_color_hex = self.domain_typography.get("accent_color", "#2563eb")
        self.current_chapter = ""

        self.page_size = self._determine_page_size()
        (
            self.inner_margin,
            self.outer_margin,
            self.top_margin,
            self.bottom_margin,
        ) = self._determine_margins()
        self.brand_palette = self._compose_brand_palette()

        self.google_fonts = GoogleFontsIntegration()
        self.setup_fonts()
        self.typography_scale = self._build_typography_scale()
        self.setup_styles()

    def setup_fonts(self):
        """Register fonts dynamically and honor domain typography defaults."""
        self.header_font = None
        self.body_font = None

        if self.font_theme:
            self.header_font = self.google_fonts.load_google_font(
                self.font_theme.header_font,
                self.font_theme.header_weight,
            )
            self.body_font = self.google_fonts.load_google_font(
                self.font_theme.body_font,
                self.font_theme.body_weight,
            )

            if not self.header_font:
                self.header_font = self.google_fonts.get_fallback_font(self.font_theme.category)
            if not self.body_font:
                self.body_font = self.google_fonts.get_fallback_font(self.font_theme.category)

            logger.info(
                "Using font theme: %s (Header: %s, Body: %s)",
                getattr(self.font_theme, "name", "custom"),
                self.header_font,
                self.body_font,
            )

        if not self.header_font:
            self.header_font = self._resolve_domain_font(
                "interior_title_font_family",
                "interior_title_weight",
                "interior_title_font",
                "title_category",
            )
        if not self.body_font:
            self.body_font = self._resolve_domain_font(
                "interior_body_font_family",
                "interior_body_weight",
                "interior_body_font",
                "body_category",
            )

        # Ensure fallbacks are registered fonts
        if not self._font_available(self.header_font):
            self.header_font = "Helvetica-Bold"
        if not self._font_available(self.body_font):
            self.body_font = "Helvetica"

    def _build_typography_scale(self) -> Dict[str, int]:
        """Define a consistent typographic scale used throughout the book."""
        return {
            'display': 44,
            'headline': 28,
            'subhead': 18,
            'body': 14,
            'small': 10,
        }

    def _font_available(self, font_name: str) -> bool:
        try:
            pdfmetrics.getFont(font_name)
            return True
        except KeyError:
            return False

    def _resolve_domain_font(
        self,
        family_key: str,
        weight_key: str,
        fallback_key: str,
        category_key: str,
    ) -> str:
        family = self.domain_typography.get(family_key)
        weight_value = self.domain_typography.get(weight_key, 400)
        fallback = self.domain_typography.get(fallback_key)
        category = self.domain_typography.get(category_key, "clean_sans")

        try:
            weight = int(weight_value)
        except (TypeError, ValueError):
            weight = 400

        if family:
            loaded = self.google_fonts.load_google_font(family, weight)
            if loaded:
                return loaded

        if fallback and self._font_available(fallback):
            return fallback

        return self.google_fonts.get_fallback_font(category)
    
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
            
            domain_slug = book.domain.slug if getattr(book, 'domain', None) else ""
            return cls(font_theme=font_theme, domain_slug=domain_slug)
            
        except Exception as e:
            logger.error(f"Font theme selection failed: {str(e)}, using defaults")
            domain_slug = book.domain.slug if getattr(book, 'domain', None) else ""
            return cls(domain_slug=domain_slug)  # Fallback to default fonts

    def setup_styles(self):
        """Create professional paragraph styles with domain accenting."""
        self.styles = self.create_enhanced_styles()

    def create_enhanced_styles(self):
        """Create domain-specific styles with callouts and hierarchy."""
        styles = getSampleStyleSheet()
        accent = HexColor(self.accent_color_hex)
        neutral = HexColor('#1f2937')
        subtitle_color = HexColor('#6b7280')

        styles.add(ParagraphStyle(
            name='BookTitle',
            parent=styles['Title'],
            fontSize=self.typography_scale['display'],
            textColor=accent,
            spaceAfter=self.typography_scale['body'] * 1.8,
            alignment=TA_CENTER,
            fontName=self.header_font,
            leading=int(self.typography_scale['display'] * 1.15),
        ))

        styles.add(ParagraphStyle(
            name='Subtitle',
            parent=styles['BodyText'],
            fontSize=self.typography_scale['subhead'],
            textColor=subtitle_color,
            alignment=TA_CENTER,
            fontName=self.body_font,
            spaceAfter=18,
        ))

        styles.add(ParagraphStyle(
            name='ChapterTitle',
            parent=styles['Heading1'],
            fontSize=self.typography_scale['headline'],
            textColor=accent,
            spaceAfter=self.typography_scale['body'],
            spaceBefore=self.typography_scale['body'] * 1.8,
            fontName=self.header_font,
            leading=int(self.typography_scale['headline'] * 1.15),
            keepWithNext=True,
        ))

        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontSize=self.typography_scale['subhead'],
            textColor=neutral,
            spaceAfter=self.typography_scale['body'] * 0.6,
            spaceBefore=self.typography_scale['body'],
            fontName=self.header_font,
            leading=int(self.typography_scale['subhead'] * 1.15),
        ))

        styles.add(ParagraphStyle(
            name='BookBody',
            parent=styles['BodyText'],
            fontSize=self.typography_scale['body'],
            textColor=neutral,
            spaceAfter=self.typography_scale['body'] * 0.85,
            alignment=TA_JUSTIFY,
            fontName=self.body_font,
            leading=int(self.typography_scale['body'] * 1.45),
        ))

        styles.add(ParagraphStyle(
            name='BulletList',
            parent=styles['BookBody'],
            leftIndent=22,
            bulletIndent=12,
            bulletFontName=self.body_font,
            spaceAfter=self.typography_scale['body'] * 0.6,
        ))

        styles.add(ParagraphStyle(
            name='Quote',
            parent=styles['BookBody'],
            fontSize=max(self.typography_scale['body'] - 1, 12),
            textColor=HexColor('#4b5563'),
            leftIndent=36,
            rightIndent=36,
            borderColor=accent,
            borderWidth=1,
            borderPadding=12,
            borderLeft=4,
            spaceAfter=self.typography_scale['body'],
        ))

        styles.add(ParagraphStyle(
            name='CalloutBox',
            parent=styles['BookBody'],
            backColor=HexColor('#f3f4f6'),
            borderColor=accent,
            borderWidth=2,
            borderRadius=6,
            borderPadding=(10, 12, 10, 16),
            textColor=neutral,
            spaceBefore=12,
            spaceAfter=15,
        ))

        styles.add(ParagraphStyle(
            name='KeyTakeaway',
            parent=styles['BookBody'],
            fontName=self.header_font,
            textColor=accent,
            leftIndent=18,
            bulletIndent=8,
            bulletFontName='Symbol',
            bulletFontSize=11,
            spaceBefore=8,
            spaceAfter=10,
        ))

        styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=styles['BodyText'],
            fontName='Courier',
            fontSize=10,
            textColor=neutral,
            backColor=HexColor('#f9fafb'),
            borderColor=HexColor('#e5e7eb'),
            borderWidth=1,
            borderPadding=12,
            leftIndent=12,
            rightIndent=12,
            spaceBefore=8,
            spaceAfter=12,
        ))

        return styles

    def _determine_page_size(self) -> tuple:
        """Resolve the page size in points, honoring domain overrides when present."""
        requested_size = self.domain_typography.get("page_size")

        custom = self._resolve_custom_page_tuple(requested_size)
        if custom:
            return custom

        if isinstance(requested_size, str):
            key = requested_size.strip().lower()
            preset_map = {
                "a4": A4,
                "iso_a4": A4,
                "letter": letter,
                "us_letter": letter,
            }
            if key in preset_map:
                return preset_map[key]

        return (6 * inch, 9 * inch)

    def _resolve_custom_page_tuple(self, requested_size) -> Optional[tuple]:
        """Validate optional custom (width, height) pair provided in inches or points."""
        if not isinstance(requested_size, (list, tuple)) or len(requested_size) != 2:
            return None

        try:
            width = float(requested_size[0])
            height = float(requested_size[1])
        except (TypeError, ValueError):
            return None

        if width <= 0 or height <= 0:
            return None

        if width <= 10 and height <= 14:
            return (width * inch, height * inch)

        return (width, height)

    def _determine_margins(self) -> tuple:
        """Compute mirrored margins (inner/outer/top/bottom) in points."""

        def to_points(value, default_inches):
            if value is None:
                return default_inches * inch
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                return default_inches * inch
            if numeric <= 10:
                return numeric * inch
            return numeric

        inner = to_points(self.domain_typography.get("inner_margin_inches"), 1.0)
        outer = to_points(self.domain_typography.get("outer_margin_inches"), 0.8)
        top = to_points(self.domain_typography.get("top_margin_inches"), 0.9)
        bottom = to_points(self.domain_typography.get("bottom_margin_inches"), 1.1)

        return inner, outer, top, bottom

    def _compose_brand_palette(self) -> Dict[str, HexColor]:
        """Derive a small brand palette for headers/footers from the accent color."""
        accent_hex = self.accent_color_hex
        accent_color = HexColor(accent_hex)
        neutral_hex = self.domain_typography.get("neutral_color", "#475569")

        return {
            "primary": accent_color,
            "accent": accent_color,
            "muted": HexColor(neutral_hex),
            "light": HexColor(self._mix_hex(accent_hex, "#ffffff", 0.72)),
            "dark": HexColor(self._mix_hex(accent_hex, "#0f172a", 0.35)),
        }

    def _hex_to_rgb(self, value: str) -> Tuple[int, int, int]:
        sanitized = (value or "").lstrip('#')
        if len(sanitized) != 6:
            return (0, 0, 0)
        return tuple(int(sanitized[i:i+2], 16) for i in (0, 2, 4))

    def _mix_hex(self, source: str, target: str, factor: float) -> str:
        factor = max(0.0, min(1.0, factor))
        sr, sg, sb = self._hex_to_rgb(source)
        tr, tg, tb = self._hex_to_rgb(target)
        r = int(sr + (tr - sr) * factor)
        g = int(sg + (tg - sg) * factor)
        b = int(sb + (tb - sb) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def create_book_pdf(self, book, content_data: Dict, output_path: str):
        """Create professionally formatted book PDF with mirrored margins."""
        self._active_book_title = book.title
        doc = self._build_doc_template(output_path, book.title)
        story = self._build_story(book, content_data)
        doc.multiBuild(story)
        return output_path

    def _build_doc_template(self, output_path: str, book_title: str) -> BaseDocTemplate:
        outer_self = self

        class ProfessionalDocTemplate(BaseDocTemplate):
            def afterFlowable(self, flowable):
                try:
                    if isinstance(flowable, Paragraph) and flowable.style.name == 'ChapterTitle':
                        text = flowable.getPlainText()
                        self.notify('TOCEntry', (0, text, self.page))
                        self._current_chapter_title = text
                        outer_self.current_chapter = text
                except Exception:
                    pass

        doc = ProfessionalDocTemplate(
            output_path,
            pagesize=self.page_size,
            topMargin=self.top_margin,
            bottomMargin=self.bottom_margin,
        )
        doc._current_chapter_title = book_title
        self.setup_page_templates(doc)
        return doc

    def setup_page_templates(self, doc: BaseDocTemplate) -> None:
        page_width, page_height = self.page_size
        content_width = page_width - self.inner_margin - self.outer_margin
        content_height = page_height - self.top_margin - self.bottom_margin

        recto_frame = Frame(
            x1=self.inner_margin,
            y1=self.bottom_margin,
            width=content_width,
            height=content_height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id='recto_frame',
        )

        verso_frame = Frame(
            x1=self.outer_margin,
            y1=self.bottom_margin,
            width=content_width,
            height=content_height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id='verso_frame',
        )

        recto_template = PageTemplate(id='recto', frames=[recto_frame], onPage=self.add_right_page_header)
        verso_template = PageTemplate(id='verso', frames=[verso_frame], onPage=self.add_left_page_header)
        doc.addPageTemplates([recto_template, verso_template])

    def add_right_page_header(self, canvas_obj, doc_obj):
        canvas_obj.saveState()
        header_y = self.page_size[1] - self.top_margin + 14
        chapter = (getattr(doc_obj, '_current_chapter_title', '') or self.current_chapter or self._active_book_title)[:60]
        canvas_obj.setFont(self.body_font, 9)
        canvas_obj.setFillColor(HexColor('#6b7280'))
        canvas_obj.drawString(self.inner_margin, header_y, chapter)
        canvas_obj.drawRightString(self.page_size[0] - self.outer_margin, header_y, str(canvas_obj.getPageNumber()))
        canvas_obj.setStrokeColor(HexColor(self.accent_color_hex))
        canvas_obj.setLineWidth(1)
        canvas_obj.line(self.inner_margin, header_y - 4, self.page_size[0] - self.outer_margin, header_y - 4)
        canvas_obj.restoreState()

    def add_left_page_header(self, canvas_obj, doc_obj):
        canvas_obj.saveState()
        header_y = self.page_size[1] - self.top_margin + 14
        chapter = (getattr(doc_obj, '_current_chapter_title', '') or self.current_chapter or self._active_book_title)[:60]
        canvas_obj.setFont(self.body_font, 9)
        canvas_obj.setFillColor(HexColor('#6b7280'))
        canvas_obj.drawString(self.outer_margin, header_y, str(canvas_obj.getPageNumber()))
        canvas_obj.drawRightString(self.page_size[0] - self.inner_margin, header_y, chapter)
        canvas_obj.setStrokeColor(HexColor(self.accent_color_hex))
        canvas_obj.setLineWidth(1)
        canvas_obj.line(self.outer_margin, header_y - 4, self.page_size[0] - self.inner_margin, header_y - 4)
        canvas_obj.restoreState()

    def _build_story(self, book, content_data: Dict) -> List:
        story: List = []
        story.extend(self._create_title_page(book, content_data))
        story.append(PageBreak())
        story.extend(self._table_of_contents_flow())

        sections = self._collect_sections(content_data)
        if sections:
            self._ensure_recto_start(story)

        for index, (chapter_title, chapter_content) in enumerate(sections):
            story.extend(self._format_chapter(chapter_title, chapter_content))
            if index < len(sections) - 1:
                self._ensure_recto_start(story)

        return story

    def _table_of_contents_flow(self) -> List:
        flow: List = []
        flow.append(Paragraph('Table of Contents', self.styles['ChapterTitle']))
        flow.append(Spacer(1, 0.3 * inch))
        toc = TableOfContents()
        toc.levelStyles = [
            ParagraphStyle(
                name='TOCLevel0',
                parent=self.styles['BookBody'],
                fontSize=12,
                leftIndent=10,
                firstLineIndent=-10,
                spaceAfter=6,
            ),
            ParagraphStyle(
                name='TOCLevel1',
                parent=self.styles['BookBody'],
                fontSize=11,
                leftIndent=30,
                firstLineIndent=-10,
                spaceAfter=4,
            ),
        ]
        flow.append(toc)
        return flow

    def _collect_sections(self, content_data: Dict) -> List:
        sections: List = []
        introduction = content_data.get('introduction')
        if introduction:
            sections.append(('Introduction', introduction))

        for chapter in content_data.get('chapters', []):
            if isinstance(chapter, dict):
                title = chapter.get('title', 'Chapter')
                body = chapter.get('content', '')
            else:
                title = 'Chapter'
                body = chapter
            sections.append((title, body))

        conclusion = content_data.get('conclusion')
        if conclusion:
            sections.append(('Conclusion', conclusion))

        takeaways = content_data.get('takeaways')
        if takeaways:
            sections.append(('Actionable Takeaways', takeaways))

        return sections

    def _ensure_recto_start(self, story: List) -> None:
        story.append(NextPageTemplate('recto'))
        story.append(PageBreak())

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
            elements.append(Paragraph(content_data['subtitle'], self.styles['Subtitle']))

        # Domain/Category badge
        if getattr(book, 'domain', None):
            domain_badge = f"<b>{book.domain.name}</b>"
            elements.append(Paragraph(domain_badge, self.styles['Subtitle']))

        return elements

    def _format_chapter(self, title: str, content: str) -> List:
        """Format chapter with professional styling"""
        elements = []

        # Chapter Title
        elements.append(Paragraph(title, self.styles['ChapterTitle']))
        elements.append(Spacer(1, 0.12 * inch))
        elements.append(HRFlowable(width="100%", thickness=1, color=HexColor(self.accent_color_hex)))
        elements.append(Spacer(1, 0.24 * inch))

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

            idx = 0
            while idx < len(paragraphs):
                paragraph = paragraphs[idx]

                if self._is_code_fence(paragraph):
                    code_lines, idx = self._collect_code_block(paragraphs, idx)
                    if code_lines:
                        elements.append(Preformatted('\n'.join(code_lines), self.styles['CodeBlock']))
                        elements.append(Spacer(1, 0.18 * inch))
                    continue

                if self._is_bullet_line(paragraph):
                    idx = self._render_bullet_block(paragraphs, idx, elements)
                    continue

                if self._render_structured_paragraph(paragraph, elements):
                    idx += 1
                    continue

                elements.append(Paragraph(paragraph, self.styles['BookBody']))
                elements.append(Spacer(1, 0.14 * inch))
                idx += 1

        return elements

    def _is_code_fence(self, line: str) -> bool:
        return line.strip().startswith('```')

    def _collect_code_block(self, paragraphs: List[str], start_index: int) -> Tuple[List[str], int]:
        idx = start_index + 1
        code_lines: List[str] = []

        while idx < len(paragraphs) and not self._is_code_fence(paragraphs[idx]):
            code_lines.append(paragraphs[idx])
            idx += 1

        if idx < len(paragraphs) and self._is_code_fence(paragraphs[idx]):
            idx += 1

        return code_lines, idx

    def _is_bullet_line(self, line: str) -> bool:
        stripped = line.lstrip()
        return bool(re.match(r'^(?:[-*•]\s+|\d+[\.\)]\s+)', stripped))

    def _render_bullet_block(self, paragraphs: List[str], start_index: int, elements: List) -> int:
        bullet_items: List[str] = []
        idx = start_index

        while idx < len(paragraphs) and self._is_bullet_line(paragraphs[idx]):
            bullet_items.append(self._clean_bullet_text(paragraphs[idx]))
            idx += 1

        for item in bullet_items:
            if not item:
                continue
            elements.append(Paragraph(f'• {item}', self.styles['BulletList']))

        elements.append(Spacer(1, 0.16 * inch))
        return idx

    def _clean_bullet_text(self, line: str) -> str:
        stripped = line.strip()
        stripped = re.sub(r'^(?:[-*•]|\d+[\.\)])\s*', '', stripped)
        return stripped.strip()

    def _render_structured_paragraph(self, paragraph: str, elements: List) -> bool:
        lowered = paragraph.lower()

        if lowered.startswith(("key takeaway", "key takeaways", "key insight")):
            heading, remainder = self._split_heading(paragraph)
            if heading:
                elements.append(Paragraph(f"<b>{heading}</b>", self.styles['SectionHeading']))
            for item in self._split_key_takeaway_items(remainder):
                elements.append(Paragraph(f'• {item}', self.styles['KeyTakeaway']))
            elements.append(Spacer(1, 0.18 * inch))
            return True

        if lowered.startswith(("pro tip", "insight", "note", "remember", "warning", "action step")):
            elements.append(Paragraph(self._highlight_leading_phrase(paragraph), self.styles['CalloutBox']))
            elements.append(Spacer(1, 0.16 * inch))
            return True

        if lowered.startswith("quote:") or paragraph.startswith("\u201c") or paragraph.startswith('"'):
            cleaned = paragraph.replace("Quote:", "", 1).strip()
            elements.append(Paragraph(cleaned, self.styles['Quote']))
            elements.append(Spacer(1, 0.16 * inch))
            return True

        return False

    def _split_heading(self, text: str) -> Tuple[str, str]:
        if ':' in text:
            heading, remainder = text.split(':', 1)
            return heading.strip(), remainder.strip()
        return text.strip(), ""

    def _split_key_takeaway_items(self, text: str) -> List[str]:
        if not text:
            return []
        candidates = re.split(r'(?:\n|;|•|\||-)\s*', text)
        return [candidate.strip('• ').strip() for candidate in candidates if candidate.strip()]

    def _highlight_leading_phrase(self, text: str) -> str:
        if ':' not in text:
            return f"<b>{text.strip()}</b>"
        lead, remainder = text.split(':', 1)
        return f"<b>{lead.strip()}:</b> {remainder.strip()}"

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