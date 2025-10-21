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
            try:
                html = HTML(string=html_content)
                html.write_pdf(
                    str(pdf_path),
                    stylesheets=[CSS(string=self._get_base_css())]
                )
            except Exception as e:
                print(f"WeasyPrint error: {str(e)}")
                raise Exception(f"PDF generation failed: {str(e)}")
            
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
        """Modern minimalist design with geometric shapes and better typography"""
        # Split title into lines for better layout
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600;800&family=Poppins:wght@300;600;800&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 50%, {colors['accent']} 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    overflow: hidden;
                    font-family: 'Inter', sans-serif;
                }}
                
                /* Geometric background elements */
                .bg-shape-1 {{
                    position: absolute;
                    width: 800px;
                    height: 800px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 50%;
                    top: -200px;
                    right: -200px;
                    backdrop-filter: blur(40px);
                }}
                
                .bg-shape-2 {{
                    position: absolute;
                    width: 600px;
                    height: 600px;
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 30%;
                    bottom: -150px;
                    left: -150px;
                    transform: rotate(45deg);
                    backdrop-filter: blur(30px);
                }}
                
                .bg-shape-3 {{
                    position: absolute;
                    width: 400px;
                    height: 400px;
                    border: 3px solid rgba(255, 255, 255, 0.3);
                    border-radius: 50%;
                    top: 200px;
                    left: 100px;
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    color: white;
                    max-width: 1200px;
                }}
                
                .category {{
                    font-family: 'Poppins', sans-serif;
                    font-size: 48px;
                    font-weight: 300;
                    letter-spacing: 12px;
                    text-transform: uppercase;
                    margin-bottom: 80px;
                    opacity: 0.9;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
                }}
                
                .title {{
                    font-family: 'Poppins', sans-serif;
                    font-size: 140px;
                    font-weight: 800;
                    line-height: 1.1;
                    margin-bottom: 60px;
                    text-shadow: 0 4px 20px rgba(0,0,0,0.4);
                    letter-spacing: -2px;
                }}
                
                .title-line-2 {{
                    font-size: 100px;
                    font-weight: 600;
                    margin-top: 20px;
                }}
                
                .subtitle {{
                    font-size: 36px;
                    font-weight: 300;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    opacity: 0.8;
                    margin-top: 40px;
                }}
                
                .accent-bar {{
                    width: 200px;
                    height: 6px;
                    background: {colors['accent']};
                    margin: 60px auto 0;
                    border-radius: 3px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                }}
            </style>
        </head>
        <body>
            <div class="bg-shape-1"></div>
            <div class="bg-shape-2"></div>
            <div class="bg-shape-3"></div>
            <div class="content">
                <div class="category">{category}</div>
                <div class="title">{title_line1}</div>
                {f'<div class="title title-line-2">{title_line2}</div>' if title_line2 else ''}
                <div class="subtitle">Complete Guide</div>
                <div class="accent-bar"></div>
            </div>
        </body>
        </html>
        """
    
    def _bold_template(self, title, category, colors):
        """Bold typography-focused design with modern elements"""
        # Split title for better layout
        words = title.split()
        if len(words) > 3:
            title_main = ' '.join(words[:-2])
            title_sub = ' '.join(words[-2:])
        else:
            title_main = title
            title_sub = ""
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@300;600&family=Raleway:wght@300;600&display=swap');
                
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
                    font-family: 'Oswald', sans-serif;
                }}
                
                /* Top accent bar */
                .top-accent {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 80px;
                    background: {colors['accent']};
                    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                }}
                
                /* Decorative elements */
                .decorative-line {{
                    position: absolute;
                    width: 4px;
                    height: 200px;
                    background: {colors['accent']};
                    left: 120px;
                    top: 200px;
                    opacity: 0.8;
                }}
                
                .decorative-circle {{
                    position: absolute;
                    width: 100px;
                    height: 100px;
                    border: 6px solid {colors['accent']};
                    border-radius: 50%;
                    right: 150px;
                    bottom: 300px;
                    opacity: 0.6;
                }}
                
                .top-section {{
                    background: rgba(255, 255, 255, 0.95);
                    padding: 50px 80px;
                    display: inline-block;
                    align-self: flex-start;
                    border-radius: 0 20px 20px 0;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    backdrop-filter: blur(10px);
                }}
                
                .category {{
                    font-family: 'Raleway', sans-serif;
                    font-size: 42px;
                    font-weight: 600;
                    color: {colors['primary']};
                    letter-spacing: 6px;
                    text-transform: uppercase;
                    margin-bottom: 20px;
                }}
                
                .category-label {{
                    font-size: 18px;
                    color: {colors['secondary']};
                    font-weight: 300;
                    letter-spacing: 2px;
                }}
                
                .title-section {{
                    text-align: right;
                    padding-right: 100px;
                    margin-top: 100px;
                }}
                
                .title {{
                    font-family: 'Bebas Neue', sans-serif;
                    font-size: 180px;
                    line-height: 0.9;
                    color: white;
                    text-transform: uppercase;
                    letter-spacing: 6px;
                    text-shadow: 0 4px 20px rgba(0,0,0,0.5);
                    margin-bottom: 20px;
                }}
                
                .title-sub {{
                    font-size: 120px;
                    font-weight: 300;
                    margin-left: 100px;
                }}
                
                .tagline {{
                    font-family: 'Raleway', sans-serif;
                    font-size: 32px;
                    font-weight: 300;
                    color: rgba(255, 255, 255, 0.9);
                    letter-spacing: 4px;
                    text-transform: uppercase;
                    margin-top: 40px;
                    text-align: right;
                    padding-right: 100px;
                }}
                
                .bottom-bar {{
                    width: 100%;
                    height: 60px;
                    background: {colors['secondary']};
                    box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
                }}
                
                .bottom-pattern {{
                    position: absolute;
                    bottom: 60px;
                    left: 0;
                    right: 0;
                    height: 20px;
                    background: repeating-linear-gradient(
                        90deg,
                        {colors['accent']},
                        {colors['accent']} 20px,
                        transparent 20px,
                        transparent 40px
                    );
                    opacity: 0.3;
                }}
            </style>
        </head>
        <body>
            <div class="top-accent"></div>
            <div class="decorative-line"></div>
            <div class="decorative-circle"></div>
            
            <div class="top-section">
                <div class="category">{category}</div>
                <div class="category-label">Professional Guide</div>
            </div>
            
            <div class="title-section">
                <div class="title">{title_main}</div>
                {f'<div class="title title-sub">{title_sub}</div>' if title_sub else ''}
                <div class="tagline">Master Your Skills</div>
            </div>
            
            <div class="bottom-pattern"></div>
            <div class="bottom-bar"></div>
        </body>
        </html>
        """
    
    def _elegant_template(self, title, category, colors):
        """Elegant professional design with serif fonts and sophisticated layout"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Playfair+Display:wght@400;700;900&family=Lato:wght@300;400;600&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    font-family: 'Lato', sans-serif;
                }}
                
                /* Elegant border frames */
                .outer-frame {{
                    position: absolute;
                    top: 60px;
                    left: 60px;
                    right: 60px;
                    bottom: 60px;
                    border: 8px solid {colors['primary']};
                    border-radius: 20px;
                    box-shadow: 0 0 50px rgba(0,0,0,0.1);
                }}
                
                .inner-frame {{
                    position: absolute;
                    top: 90px;
                    left: 90px;
                    right: 90px;
                    bottom: 90px;
                    border: 3px solid {colors['secondary']};
                    border-radius: 15px;
                }}
                
                .decorative-corner {{
                    position: absolute;
                    width: 40px;
                    height: 40px;
                    border: 4px solid {colors['accent']};
                    top: 100px;
                    right: 100px;
                    border-radius: 50% 0 50% 0;
                    transform: rotate(45deg);
                }}
                
                .decorative-corner2 {{
                    position: absolute;
                    width: 30px;
                    height: 30px;
                    background: {colors['accent']};
                    bottom: 120px;
                    left: 120px;
                    border-radius: 50%;
                    opacity: 0.7;
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    color: {colors['primary']};
                    max-width: 1000px;
                }}
                
                .category {{
                    font-family: 'Lato', sans-serif;
                    font-size: 48px;
                    font-weight: 300;
                    letter-spacing: 15px;
                    text-transform: uppercase;
                    margin-bottom: 100px;
                    color: {colors['secondary']};
                    opacity: 0.8;
                }}
                
                .title {{
                    font-family: 'Playfair Display', serif;
                    font-size: 120px;
                    font-weight: 900;
                    line-height: 1.1;
                    margin-bottom: 60px;
                    letter-spacing: 2px;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                
                .subtitle {{
                    font-family: 'Crimson Text', serif;
                    font-size: 32px;
                    font-style: italic;
                    color: {colors['secondary']};
                    margin-bottom: 80px;
                    letter-spacing: 1px;
                }}
                
                .ornament {{
                    width: 200px;
                    height: 4px;
                    background: linear-gradient(90deg, transparent, {colors['accent']}, transparent);
                    margin: 0 auto 60px;
                    position: relative;
                }}
                
                .ornament::before {{
                    content: '';
                    position: absolute;
                    width: 12px;
                    height: 12px;
                    background: {colors['accent']};
                    border-radius: 50%;
                    left: -6px;
                    top: -4px;
                }}
                
                .ornament::after {{
                    content: '';
                    position: absolute;
                    width: 12px;
                    height: 12px;
                    background: {colors['accent']};
                    border-radius: 50%;
                    right: -6px;
                    top: -4px;
                }}
                
                .tagline {{
                    font-family: 'Lato', sans-serif;
                    font-size: 24px;
                    font-weight: 300;
                    letter-spacing: 6px;
                    text-transform: uppercase;
                    color: {colors['secondary']};
                    opacity: 0.7;
                }}
            </style>
        </head>
        <body>
            <div class="outer-frame"></div>
            <div class="inner-frame"></div>
            <div class="decorative-corner"></div>
            <div class="decorative-corner2"></div>
            
            <div class="content">
                <div class="category">{category}</div>
                <h1 class="title">{title}</h1>
                <div class="subtitle">A Comprehensive Guide to Excellence</div>
                <div class="ornament"></div>
                <div class="tagline">Professional Insights</div>
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
            # Make sure pdf2image is available
            import importlib.util
            pdf2image_spec = importlib.util.find_spec('pdf2image')
            if pdf2image_spec is not None:
                try:
                    from pdf2image import convert_from_path
                    images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
                    if images:
                        images[0].save(png_path, 'PNG')
                        print(f"Successfully converted PDF to PNG: {png_path}")
                        return
                except Exception as e:
                    print(f"pdf2image conversion failed: {e}, trying alternative method")
            else:
                print("pdf2image module not found, using fallback method")
                
            # Try alternative method using Pillow directly
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(pdf_path)
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                pix.save(png_path)
                print(f"PyMuPDF successfully saved PNG: {png_path}")
                return
            except ImportError:
                print("PyMuPDF not available, using simple fallback")
            except Exception as e:
                print(f"PyMuPDF conversion failed: {e}")
                
        except Exception as e:
            print(f"Error converting PDF to PNG: {e}")
            
        # Fallback: Create a simple preview image using PIL
        try:
            img = Image.new('RGB', (600, 900), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to load a font
            try:
                font = ImageFont.truetype("Arial", 40)
            except:
                font = ImageFont.load_default()
                
            # Draw placeholder text
            draw.rectangle([50, 50, 550, 850], outline="black", width=5)
            draw.text((300, 300), "Cover Preview", fill='black', font=font, anchor="mm")
            draw.text((300, 400), "Image generation", fill='black', font=font, anchor="mm")
            draw.text((300, 500), "in progress", fill='black', font=font, anchor="mm")
            
            img.save(png_path, 'PNG')
            print(f"Created fallback image: {png_path}")
        except Exception as e:
            print(f"Error creating fallback image: {e}")
