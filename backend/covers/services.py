# covers/services.py
import os
import random
from pathlib import Path
from django.conf import settings
from weasyprint import HTML, CSS
from PIL import Image, ImageDraw, ImageFont
import io

class CoverGenerator:
    """
    Generates professional book covers using HTML/CSS templates
    No credit card required - uses WeasyPrint for rendering
    """
    
    # Color schemes for each sub-niche
    NICHE_COLORS = {
        # Language and Kids - Playful, bright, educational colors
        'ai_learning_stories': {'primary': '#FF6B9D', 'secondary': '#C44569', 'accent': '#FFA07A'},
        'multilingual_coloring': {'primary': '#4ECDC4', 'secondary': '#44A08D', 'accent': '#F7B731'},
        'kids_mindful_journals': {'primary': '#A8E6CF', 'secondary': '#78E08F', 'accent': '#FDCB6E'},
        
        # Technology and AI - Modern, tech-inspired, professional
        'ai_ethics': {'primary': '#2C3A47', 'secondary': '#2F3542', 'accent': '#3B82F6'},
        'nocode_guides': {'primary': '#5F27CD', 'secondary': '#341F97', 'accent': '#00D2D3'},
        'smart_home_diy': {'primary': '#1E3A8A', 'secondary': '#3B82F6', 'accent': '#60A5FA'},
        
        # Nutrition and Wellness - Fresh, healthy, appetizing
        'specialty_diet': {'primary': '#FF6348', 'secondary': '#FF4757', 'accent': '#FFA502'},
        'plant_based_cooking': {'primary': '#6BCB77', 'secondary': '#4D96A9', 'accent': '#FFD93D'},
        'nutrition_mental_health': {'primary': '#A29BFE', 'secondary': '#6C5CE7', 'accent': '#FD79A8'},
        
        # Meditation - Calming, peaceful, zen-like
        'mindfulness_anxiety': {'primary': '#74B9FF', 'secondary': '#A29BFE', 'accent': '#DFE6E9'},
        'sleep_meditation': {'primary': '#4834D4', 'secondary': '#686DE0', 'accent': '#95AAD'},
        'gratitude_journals': {'primary': '#FAD390', 'secondary': '#F8C291', 'accent': '#6A89CC'},
        
        # Home Workout - Energetic, motivational, strong
        'equipment_free': {'primary': '#EE5A6F', 'secondary': '#C44569', 'accent': '#F8B500'},
        'yoga_remote_workers': {'primary': '#0ABDE3', 'secondary': '#48DBFB', 'accent': '#1DD1A1'},
        'mobility_training': {'primary': '#FF9FF3', 'secondary': '#54A0FF', 'accent': '#48DBFB'},
    }
    
    # Template styles
    TEMPLATE_STYLES = ['modern', 'bold', 'elegant']
    
    def __init__(self):
        self.media_root = Path(settings.MEDIA_ROOT)
        self.covers_dir = self.media_root / 'covers'
        self.covers_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_three_covers(self, book):
        """
        Generate 3 different cover designs for a book
        Returns list of Cover objects
        """
        from covers.models import Cover
        
        covers = []
        colors = self.NICHE_COLORS.get(book.sub_niche, {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'accent': '#ECF0F1'
        })
        
        for template_style in self.TEMPLATE_STYLES:
            # Generate unique filename
            filename = f"book_{book.id}_{template_style}_{random.randint(1000, 9999)}"
            image_path = self.covers_dir / f"{filename}.png"
            pdf_path = self.covers_dir / f"{filename}.pdf"
            
            # Generate HTML
            html_content = self._generate_html_template(
                title=book.title,
                sub_niche=book.sub_niche,
                colors=colors,
                template_style=template_style
            )
            
            # Render to PDF first (better quality)
            HTML(string=html_content).write_pdf(
                str(pdf_path),
                stylesheets=[CSS(string=self._get_base_css())]
            )
            
            # Convert PDF to PNG for preview
            self._pdf_to_png(str(pdf_path), str(image_path))
            
            # Create Cover object
            cover = Cover.objects.create(
                book=book,
                template_style=template_style,
                image_path=f"covers/{image_path.name}",
                pdf_path=f"covers/{pdf_path.name}",
                generation_params={
                    'colors': colors,
                    'template': template_style,
                }
            )
            covers.append(cover)
        
        return covers
    
    def _generate_html_template(self, title, sub_niche, colors, template_style):
        """Generate HTML for cover based on template style"""
        
        # Get niche display name
        niche_display = dict([
            ('yoga_beginners', 'Yoga & Fitness'),
            ('home_workouts', 'Fitness & Health'),
            ('mental_wellness', 'Wellness & Mindfulness'),
            ('vegan_recipes', 'Plant-Based Cooking'),
            ('meal_prep', 'Meal Planning'),
            ('smoothie_recipes', 'Healthy Beverages'),
            ('productivity', 'Productivity & Success'),
            ('morning_routines', 'Personal Growth'),
            ('goal_setting', 'Achievement & Goals'),
            ('gardening', 'Gardening & Nature'),
            ('photography', 'Photography & Art'),
            ('diy_crafts', 'Crafts & DIY'),
            ('minimalism', 'Lifestyle & Design'),
            ('sustainable_living', 'Eco-Living'),
            ('travel_hacks', 'Travel & Adventure'),
        ]).get(sub_niche, 'Lifestyle')
        
        if template_style == 'modern':
            return self._modern_template(title, niche_display, colors)
        elif template_style == 'bold':
            return self._bold_template(title, niche_display, colors)
        else:
            return self._elegant_template(title, niche_display, colors)
    
    def _modern_template(self, title, category, colors):
        """Modern minimalist design with geometric shapes"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600;800&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 100px;
                    position: relative;
                    overflow: hidden;
                }}
                
                .geometric-bg {{
                    position: absolute;
                    width: 600px;
                    height: 600px;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.1);
                    top: -200px;
                    right: -200px;
                }}
                
                .geometric-bg2 {{
                    position: absolute;
                    width: 400px;
                    height: 400px;
                    border-radius: 30%;
                    background: rgba(255, 255, 255, 0.08);
                    bottom: -100px;
                    left: -100px;
                    transform: rotate(45deg);
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    color: white;
                }}
                
                .category {{
                    font-size: 42px;
                    font-weight: 300;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    margin-bottom: 60px;
                    opacity: 0.9;
                }}
                
                .title {{
                    font-size: 120px;
                    font-weight: 800;
                    line-height: 1.2;
                    margin-bottom: 100px;
                    text-shadow: 0 4px 20px rgba(0,0,0,0.2);
                }}
                
                .accent-line {{
                    width: 300px;
                    height: 8px;
                    background: {colors['accent']};
                    margin: 0 auto;
                }}
            </style>
        </head>
        <body>
            <div class="geometric-bg"></div>
            <div class="geometric-bg2"></div>
            <div class="content">
                <div class="category">{category}</div>
                <h1 class="title">{title}</h1>
                <div class="accent-line"></div>
            </div>
        </body>
        </html>
        """
    
    def _bold_template(self, title, category, colors):
        """Bold typography-focused design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;700&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: {colors['primary']};
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    padding: 120px 100px;
                    position: relative;
                }}
                
                .top-section {{
                    background: {colors['accent']};
                    padding: 40px 60px;
                    display: inline-block;
                    align-self: flex-start;
                }}
                
                .category {{
                    font-family: 'Roboto', sans-serif;
                    font-size: 38px;
                    font-weight: 700;
                    color: {colors['primary']};
                    letter-spacing: 4px;
                    text-transform: uppercase;
                }}
                
                .title {{
                    font-family: 'Bebas Neue', sans-serif;
                    font-size: 160px;
                    line-height: 0.95;
                    color: white;
                    text-transform: uppercase;
                    letter-spacing: 4px;
                    padding: 0 60px;
                }}
                
                .bottom-bar {{
                    width: 100%;
                    height: 40px;
                    background: {colors['secondary']};
                }}
            </style>
        </head>
        <body>
            <div class="top-section">
                <div class="category">{category}</div>
            </div>
            <div class="title">{title}</div>
            <div class="bottom-bar"></div>
        </body>
        </html>
        """
    
    def _elegant_template(self, title, category, colors):
        """Elegant professional design with serif fonts"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: white;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                }}
                
                .border-frame {{
                    position: absolute;
                    top: 80px;
                    left: 80px;
                    right: 80px;
                    bottom: 80px;
                    border: 6px solid {colors['primary']};
                }}
                
                .inner-border {{
                    position: absolute;
                    top: 100px;
                    left: 100px;
                    right: 100px;
                    bottom: 100px;
                    border: 2px solid {colors['secondary']};
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    color: {colors['primary']};
                }}
                
                .category {{
                    font-family: 'Lato', sans-serif;
                    font-size: 38px;
                    font-weight: 300;
                    letter-spacing: 12px;
                    text-transform: uppercase;
                    margin-bottom: 80px;
                    color: {colors['secondary']};
                }}
                
                .title {{
                    font-family: 'Playfair Display', serif;
                    font-size: 110px;
                    font-weight: 900;
                    line-height: 1.2;
                    margin-bottom: 80px;
                }}
                
                .ornament {{
                    width: 150px;
                    height: 150px;
                    margin: 0 auto;
                    border: 4px solid {colors['accent']};
                    border-radius: 50%;
                    background: linear-gradient(135deg, {colors['secondary']}, {colors['accent']});
                }}
            </style>
        </head>
        <body>
            <div class="border-frame"></div>
            <div class="inner-border"></div>
            <div class="content">
                <div class="category">{category}</div>
                <h1 class="title">{title}</h1>
                <div class="ornament"></div>
            </div>
        </body>
        </html>
        """
    
    def _get_base_css(self):
        """Base CSS for PDF rendering"""
        return """
        @page {
            size: 6in 9in;
            margin: 0;
        }
        """
    
    def _pdf_to_png(self, pdf_path, png_path):
        """Convert first page of PDF to PNG for preview"""
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
            if images:
                images[0].save(png_path, 'PNG')
        except ImportError:
            # Fallback: Create a simple preview image using PIL
            img = Image.new('RGB', (600, 900), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((300, 450), "Cover Preview", fill='black', anchor='mm')
            img.save(png_path, 'PNG')
