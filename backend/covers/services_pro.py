from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color
from pathlib import Path
from django.conf import settings
from .models import Cover

class CoverGeneratorProfessional:
    """
    Generate magazine-quality book covers with 3 distinct professional styles
    """

    def __init__(self):
        self.setup_fonts()
        self.cover_styles = {
            'minimalist': {
                'name': 'Minimalist',
                'background': '#ffffff',
                'primary': '#1a365d',
                'accent': '#e2e8f0',
                'text': '#1a365d',
                'secondary_text': '#64748b',
                'features': ['clean_lines', 'negative_space', 'simple_geometry']
            },
            'futuristic': {
                'name': 'Futuristic',
                'background': '#0f172a',
                'primary': '#06b6d4',
                'accent': '#22d3ee',
                'text': '#ffffff',
                'secondary_text': '#cbd5e1',
                'features': ['gradients', 'geometric_shapes', 'tech_elements']
            },
            'professional': {
                'name': 'Professional',
                'background': '#1e293b',
                'primary': '#3b82f6',
                'accent': '#60a5fa',
                'text': '#ffffff',
                'secondary_text': '#94a3b8',
                'features': ['corporate_colors', 'clean_layout', 'trust_elements']
            }
        }

    def setup_fonts(self):
        """Register professional fonts for covers"""
        font_paths = {
            'Montserrat-ExtraBold': '/usr/share/fonts/truetype/montserrat/Montserrat-ExtraBold.ttf',
            'Montserrat-Bold': '/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf',
            'Montserrat-Medium': '/usr/share/fonts/truetype/montserrat/Montserrat-Medium.ttf',
            'Montserrat-Regular': '/usr/share/fonts/truetype/montserrat/Montserrat-Regular.ttf',
        }

        for font_name, font_path in font_paths.items():
            try:
                if Path(font_path).exists():
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
            except Exception as e:
                print(f"Font load warning: {e}")

    def generate_three_covers(self, book):
        """
        Generate 3 distinct professional covers for a book
        Returns list of Cover model instances
        """
        covers = []
        
        for style_name, style_config in self.cover_styles.items():
            try:
                # Generate cover PDF
                cover_path = self._generate_cover_pdf(book, style_name, style_config)
                
                # Generate cover image (PNG) for preview
                image_path = self._generate_cover_image(book, style_name, style_config)
                
                # Create Cover model instance
                cover = Cover.objects.create(
                    book=book,
                    template_style=style_name,
                    image_path=image_path,
                    pdf_path=cover_path,
                    generation_params={
                        'style': style_name,
                        'colors': style_config,
                        'features': style_config['features']
                    }
                )
                
                covers.append(cover)
                print(f"Generated {style_name} cover for book {book.id}")
                
            except Exception as e:
                print(f"Failed to generate {style_name} cover: {str(e)}")
                continue
        
        return covers

    def generate_single_cover(self, book):
        """
        Generate a single cover (for guided workflow)
        Uses professional style by default
        """
        print(f"DEBUG: generate_single_cover called for book {book.id}")
        print(f"DEBUG: book.domain = {book.domain}")
        print(f"DEBUG: book.niche = {book.niche}")
        
        style_name = 'professional'
        style_config = self.cover_styles[style_name]
        
        # Generate cover PDF
        cover_path = self._generate_cover_pdf(book, style_name, style_config)
        
        # Generate cover image (PNG) for preview
        image_path = self._generate_cover_image(book, style_name, style_config)
        
        # Create Cover model instance
        cover = Cover.objects.create(
            book=book,
            template_style=style_name,
            image_path=image_path,
            pdf_path=cover_path,
            generation_params={
                'style': style_name,
                'colors': style_config,
                'features': style_config['features']
            }
        )
        
        # Auto-select this cover for guided workflow
        cover.select()
        
        return cover

    def _generate_cover_pdf(self, book, style_name, style_config):
        """Generate PDF cover for the given style"""
        print(f"DEBUG: Generating cover for book {book.id}, domain: {book.domain}, niche: {book.niche}")
        
        # Create media/covers directory if it doesn't exist
        covers_dir = Path(settings.MEDIA_ROOT) / 'covers'
        covers_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        filename = f"cover_{book.id}_{style_name}.pdf"
        output_path = covers_dir / filename
        
        c = canvas.Canvas(str(output_path), pagesize=letter)
        width, height = letter
        
        # Draw background based on style
        self._draw_background(c, width, height, style_config, style_name)
        
        # Draw decorative elements based on style
        self._draw_decorative_elements(c, width, height, style_config, style_name)
        
        # Draw title with style-specific formatting
        self._draw_title(c, book.title, width, height, style_config, style_name)
        
        # Draw domain/subject badge
        print(f"DEBUG: About to access book.domain.name")
        print(f"DEBUG: book.domain = {book.domain}")
        print(f"DEBUG: book.domain is None? {book.domain is None}")
        if book.domain:
            print(f"DEBUG: book.domain.name = {book.domain.name}")
        domain_name = book.domain.name if book.domain else 'General'
        print(f"DEBUG: domain_name = {domain_name}")
        self._draw_domain_badge(c, domain_name, width, height, style_config, style_name)
        
        c.save()
        return f"covers/{filename}"

    def _generate_cover_image(self, book, style_name, style_config):
        """Generate PNG image preview for the cover"""
        # For now, return the PDF path - frontend can handle PDF preview
        # In production, you might want to convert PDF to PNG using a library like pdf2image
        return f"covers/cover_{book.id}_{style_name}.pdf"

    def _draw_background(self, c, width, height, colors, style_name):
        """Draw background based on style"""
        if style_name == 'minimalist':
            # Clean white background with subtle accent
            c.setFillColor(HexColor(colors['background']))
            c.rect(0, 0, width, height, fill=1)
            
            # Subtle accent stripe
            c.setFillColor(HexColor(colors['accent']))
            c.rect(0, height * 0.85, width, height * 0.15, fill=1)
            
        elif style_name == 'futuristic':
            # Dark gradient background
            self._draw_gradient_background(c, width, height, colors)
            
        elif style_name == 'professional':
            # Corporate blue gradient
            c.setFillColor(HexColor(colors['background']))
            c.rect(0, 0, width, height, fill=1)
            
            # Professional accent overlay
            primary_color = HexColor(colors['primary'])
            translucent_primary = Color(primary_color.red, primary_color.green, primary_color.blue, alpha=0.1)
            c.setFillColor(translucent_primary)
            c.rect(width * 0.7, 0, width * 0.3, height, fill=1)

    def _draw_gradient_background(self, c, width, height, colors):
        """Draw gradient background for futuristic style"""
        # Create gradient effect using multiple rectangles with decreasing opacity
        base_color = HexColor(colors['background'])
        accent_color = HexColor(colors['primary'])
        
        # Base dark background
        c.setFillColor(base_color)
        c.rect(0, 0, width, height, fill=1)
        
        # Gradient overlay
        for i in range(10):
            alpha = 0.1 - (i * 0.008)  # Decreasing opacity
            c.setFillColor(Color(accent_color.red, accent_color.green, accent_color.blue, alpha))
            y_pos = height - (i * height * 0.1)
            c.rect(0, y_pos, width, height * 0.1, fill=1)

    def _draw_decorative_elements(self, c, width, height, colors, style_name):
        """Draw decorative elements based on style"""
        c.setStrokeColor(HexColor(colors['accent']))
        
        if style_name == 'minimalist':
            # Simple geometric lines
            c.setLineWidth(2)
            c.setStrokeColor(HexColor(colors['primary']))
            
            # Horizontal lines
            for i in range(3):
                y = height * 0.2 + (i * height * 0.15)
                c.line(width * 0.1, y, width * 0.9, y)
                
        elif style_name == 'futuristic':
            # Tech geometric shapes
            c.setLineWidth(3)
            c.setStrokeColor(HexColor(colors['accent']))
            
            # Diagonal lines
            for i in range(5):
                y_start = height - (i * height/6)
                c.line(0, y_start, width * 0.4, y_start - height * 0.15)
            
            # Circles
            accent_color = HexColor(colors['accent'])
            translucent_accent = Color(accent_color.red, accent_color.green, accent_color.blue, alpha=0.3)
            c.setFillColor(translucent_accent)
            c.circle(width * 0.8, height * 0.2, width * 0.08, fill=1)
            c.circle(width * 0.85, height * 0.25, width * 0.05, fill=1)
            
        elif style_name == 'professional':
            # Corporate elements
            c.setLineWidth(4)
            c.setStrokeColor(HexColor(colors['primary']))
            
            # Corner accent
            c.line(width * 0.8, height * 0.9, width * 0.9, height * 0.9)
            c.line(width * 0.9, height * 0.9, width * 0.9, height * 0.8)

    def _draw_title(self, c, title, width, height, colors, style_name):
        """Draw title with style-specific formatting"""
        # Intelligent text wrapping
        words = title.split()
        max_chars_per_line = 18 if style_name == 'minimalist' else 22
        
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
        
        # Style-specific font and sizing
        if style_name == 'minimalist':
            font_name = 'Montserrat-ExtraBold' if 'Montserrat-ExtraBold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
            base_font_size = 52 if len(lines) <= 2 else 44
        elif style_name == 'futuristic':
            font_name = 'Montserrat-Bold' if 'Montserrat-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
            base_font_size = 48 if len(lines) <= 2 else 40
        else:  # professional
            font_name = 'Montserrat-ExtraBold' if 'Montserrat-ExtraBold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
            base_font_size = 50 if len(lines) <= 2 else 42
        
        # Adjust for line count
        if len(lines) > 3:
            base_font_size *= 0.85
        
        c.setFillColor(HexColor(colors['text']))
        c.setFont(font_name, base_font_size)
        
        # Style-specific positioning
        if style_name == 'minimalist':
            # Centered, high on page
            total_height = len(lines) * (base_font_size * 1.3)
            start_y = height * 0.75 + total_height / 2
        elif style_name == 'futuristic':
            # Slightly offset for dynamic feel
            total_height = len(lines) * (base_font_size * 1.2)
            start_y = height * 0.65 + total_height / 2
        else:  # professional
            # Traditional centered
            total_height = len(lines) * (base_font_size * 1.25)
            start_y = height / 2 + total_height / 2
        
        # Draw each line
        for i, line in enumerate(lines):
            y = start_y - (i * base_font_size * 1.3)
            
            if style_name == 'minimalist':
                # Perfect center
                text_width = c.stringWidth(line, font_name, base_font_size)
                x = (width - text_width) / 2
            elif style_name == 'futuristic':
                # Slight left offset for modern feel
                text_width = c.stringWidth(line, font_name, base_font_size)
                x = (width - text_width) / 2 - width * 0.02
            else:
                # Center
                text_width = c.stringWidth(line, font_name, base_font_size)
                x = (width - text_width) / 2
                
            c.drawString(x, y, line)

    def _draw_domain_badge(self, c, domain_name, width, height, colors, style_name):
        """Draw domain/subject badge with style-specific design"""
        print(f"DEBUG: Drawing domain badge for: {domain_name}")
        
        badge_width = width * 0.35
        badge_height = 45
        
        # Style-specific positioning
        if style_name == 'minimalist':
            badge_x = (width - badge_width) / 2
            badge_y = height * 0.18
        elif style_name == 'futuristic':
            badge_x = width * 0.1
            badge_y = height * 0.15
        else:  # professional
            badge_x = (width - badge_width) / 2
            badge_y = height * 0.15
        
        # Style-specific badge design
        if style_name == 'minimalist':
            # Simple rectangle with border
            c.setStrokeColor(HexColor(colors['primary']))
            c.setLineWidth(2)
            c.setFillColor(HexColor(colors['background']))
            c.rect(badge_x, badge_y, badge_width, badge_height, fill=1, stroke=1)
            
            text_color = colors['primary']
            
        elif style_name == 'futuristic':
            # Rounded rectangle with gradient effect
            c.setFillColor(HexColor(colors['accent']))
            c.roundRect(badge_x, badge_y, badge_width, badge_height, 8, fill=1)
            
            # Inner highlight
            c.setFillColor(Color(1, 1, 1, 0.2))
            c.roundRect(badge_x + 2, badge_y + badge_height - 15, badge_width - 4, 12, 6, fill=1)
            
            text_color = colors['background']
            
        else:  # professional
            # Clean rounded badge
            c.setFillColor(HexColor(colors['accent']))
            c.roundRect(badge_x, badge_y, badge_width, badge_height, 6, fill=1)
            text_color = colors['background']
        
        # Badge text
        font_name = 'Montserrat-Bold' if 'Montserrat-Bold' in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
        c.setFont(font_name, 13)
        c.setFillColor(HexColor(text_color))
        
        text_width = c.stringWidth(domain_name.upper(), font_name, 13)
        text_x = badge_x + (badge_width - text_width) / 2
        text_y = badge_y + (badge_height - 13) / 2 + 2
        
        c.drawString(text_x, text_y, domain_name.upper())