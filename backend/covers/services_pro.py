from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap
from pathlib import Path

class ProfessionalCoverGenerator:
    """
    Generate magazine-quality book covers
    """

    def __init__(self):
        self.setup_fonts()
        self.color_schemes = {
            'ai_tech': {
                'background': '#0f172a',
                'primary': '#3b82f6',
                'accent': '#60a5fa',
                'text': '#ffffff'
            },
            'sustainability': {
                'background': '#064e3b',
                'primary': '#10b981',
                'accent': '#6ee7b7',
                'text': '#ffffff'
            },
            'mental_health': {
                'background': '#1e293b',
                'primary': '#8b5cf6',
                'accent': '#c4b5fd',
                'text': '#ffffff'
            },
            'future_skills': {
                'background': '#1e1b4b',
                'primary': '#6366f1',
                'accent': '#a5b4fc',
                'text': '#ffffff'
            },
            'default': {
                'background': '#1a365d',
                'primary': '#3182ce',
                'accent': '#90cdf4',
                'text': '#ffffff'
            }
        }

    def setup_fonts(self):
        """Register professional fonts for covers"""
        font_paths = {
            'Montserrat-ExtraBold': '/usr/share/fonts/truetype/montserrat/Montserrat-ExtraBold.ttf',
            'Montserrat-Bold': '/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf',
            'Montserrat-Medium': '/usr/share/fonts/truetype/montserrat/Montserrat-Medium.ttf',
        }

        for font_name, font_path in font_paths.items():
            try:
                if Path(font_path).exists():
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
            except Exception as e:
                print(f"Font load warning: {e}")

    def generate_cover(self, book, output_path: str):
        """Generate professional book cover"""
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # Get color scheme based on domain
        domain_slug = book.domain.slug if book.domain else 'default'
        colors = self.color_schemes.get(domain_slug, self.color_schemes['default'])

        # Background
        self._draw_background(c, width, height, colors)

        # Decorative elements
        self._draw_design_elements(c, width, height, colors)

        # Title with intelligent wrapping
        self._draw_title(c, book.title, width, height, colors)

        # Domain badge
        self._draw_domain_badge(c, book.domain.name if book.domain else '', width, height, colors)

        # Finish
        c.save()
        return output_path

    def _draw_background(self, c, width, height, colors):
        """Draw gradient-like background"""
        # Base color
        c.setFillColor(HexColor(colors['background']))
        c.rect(0, 0, width, height, fill=1)

        # Accent overlay
        c.setFillColor(HexColor(colors['primary'] + '40'))  # 25% opacity simulation
        c.rect(width * 0.6, 0, width * 0.4, height, fill=1)

    def _draw_design_elements(self, c, width, height, colors):
        """Draw modern geometric elements"""
        c.setStrokeColor(HexColor(colors['accent']))
        c.setLineWidth(3)

        # Diagonal lines
        for i in range(3):
            y_start = height - (i * height/4)
            c.line(0, y_start, width * 0.3, y_start - height * 0.2)

        # Circle accent
        c.setFillColor(HexColor(colors['accent'] + '30'))
        c.circle(width * 0.85, height * 0.15, width * 0.12, fill=1)

    def _draw_title(self, c, title: str, width, height, colors):
        """Draw title with intelligent text wrapping and sizing"""
        # Wrap title intelligently
        words = title.split()
        max_chars_per_line = 20

        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_chars_per_line:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        # Adjust font size based on number of lines
        if len(lines) <= 2:
            font_size = 48
        elif len(lines) == 3:
            font_size = 40
        else:
            font_size = 34

        # Use professional font
        font_name = 'Montserrat-ExtraBold' if 'Montserrat-ExtraBold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'

        c.setFillColor(HexColor(colors['text']))
        c.setFont(font_name, font_size)

        # Center vertically
        total_height = len(lines) * (font_size * 1.2)
        start_y = height/2 + total_height/2

        # Draw each line
        for i, line in enumerate(lines):
            y = start_y - (i * font_size * 1.2)
            # Center horizontally
            text_width = c.stringWidth(line, font_name, font_size)
            x = (width - text_width) / 2
            c.drawString(x, y, line)

    def _draw_domain_badge(self, c, domain_name: str, width, height, colors):
        """Draw domain category badge"""
        badge_width = width * 0.4
        badge_height = 50
        badge_x = (width - badge_width) / 2
        badge_y = height * 0.15

        # Badge background
        c.setFillColor(HexColor(colors['accent']))
        c.roundRect(badge_x, badge_y, badge_width, badge_height, 10, fill=1)

        # Badge text
        c.setFillColor(HexColor(colors['background']))
        c.setFont('Montserrat-Bold' if 'Montserrat-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold', 14)

        text_width = c.stringWidth(domain_name, 'Montserrat-Bold', 14)
        text_x = badge_x + (badge_width - text_width) / 2
        text_y = badge_y + (badge_height - 14) / 2

        c.drawString(text_x, text_y, domain_name.upper())