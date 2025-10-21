# covers/services.py
import os
import json
import requests
import random
from pathlib import Path
from django.conf import settings
from weasyprint import HTML, CSS
from PIL import Image, ImageDraw, ImageFont
import io
from books.services.usage_tracker import UsageTracker

class CoverGenerator:
    """
    Generates professional book covers using AI-powered design concepts
    Creates modern, trending cover designs with OpenRouter DeepSeek R1T2 Chimera
    """
    
    # Modern design trends for 2024-2025
    DESIGN_TRENDS_2025 = {
        'minimalist_abstract': {
            'style': 'Clean geometric shapes with subtle gradients',
            'colors': ['#f8fafc', '#e2e8f0', '#64748b', '#334155'],
            'fonts': 'Sans-serif modern typography'
        },
        'glassmorphism': {
            'style': 'Frosted glass effects with transparency layers',
            'colors': ['#ffffff', '#f1f5f9', '#e2e8f0', '#cbd5e1'],
            'fonts': 'Rounded sans-serif with light weights'
        },
        'neomorphism': {
            'style': 'Soft shadows creating embedded/inset effects',
            'colors': ['#f8fafc', '#f1f5f9', '#e2e8f0', '#cbd5e1'],
            'fonts': 'Clean sans-serif with medium contrast'
        },
        'brutalist': {
            'style': 'Bold typography with high contrast and raw edges',
            'colors': ['#000000', '#ffffff', '#dc2626', '#ea580c'],
            'fonts': 'Heavy sans-serif or display fonts'
        },
        'organic_shapes': {
            'style': 'Flowing curves and natural forms',
            'colors': ['#10b981', '#059669', '#047857', '#064e3b'],
            'fonts': 'Humanist sans-serif with warm feel'
        },
        'cyberpunk': {
            'style': 'Neon accents on dark backgrounds with tech elements',
            'colors': ['#000000', '#1f2937', '#7c3aed', '#ec4899'],
            'fonts': 'Futuristic sans-serif with condensed widths'
        },
        'vintage_modern': {
            'style': 'Retro color palettes with contemporary typography',
            'colors': ['#fef3c7', '#fde68a', '#f59e0b', '#d97706'],
            'fonts': 'Classic serif with modern spacing'
        }
    }
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "deepseek/deepseek-chat"
        self.usage_tracker = UsageTracker()
        self.media_root = Path(settings.MEDIA_ROOT)
        self.covers_dir = self.media_root / 'covers'
        self.covers_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_three_covers(self, book):
        """
        Generate 3 different AI-powered cover designs for a book
        Returns list of Cover objects with professional design concepts
        """
        from covers.models import Cover
        
        covers = []
        
        # Generate 3 unique design concepts using AI
        design_concepts = self._generate_ai_cover_concepts(book)
        
        for i, concept in enumerate(design_concepts):
            # Generate unique filename
            filename = f"book_{book.id}_ai_cover_{i+1}_{random.randint(1000, 9999)}"
            image_path = self.covers_dir / f"{filename}.png"
            pdf_path = self.covers_dir / f"{filename}.pdf"
            
            # Create HTML with AI-generated design
            html_content = self._create_ai_cover_html(book.title, concept)
            
            try:
                # Render to PDF
                html = HTML(string=html_content)
                html.write_pdf(
                    str(pdf_path),
                    stylesheets=[CSS(string=self._get_modern_css())]
                )
                
                # Convert PDF to PNG for preview
                self._pdf_to_png(str(pdf_path), str(image_path))
                
                # Create Cover object
                cover = Cover.objects.create(
                    book=book,
                    template_style=f"ai_concept_{i+1}",
                    image_path=f"covers/{image_path.name}",
                    pdf_path=f"covers/{pdf_path.name}",
                    generation_params={
                        'ai_generated': True,
                        'design_concept': concept,
                        'trend_style': concept.get('trend', 'modern'),
                        'colors': concept.get('colors', {}),
                    }
                )
                covers.append(cover)
                
            except Exception as e:
                print(f"Cover generation failed for concept {i+1}: {str(e)}")
                # Create fallback cover
                fallback_cover = self._create_fallback_cover(book, i+1)
                if fallback_cover:
                    covers.append(fallback_cover)
        
        return covers
    
    def _generate_ai_cover_concepts(self, book):
        """Generate AI-powered cover design concepts using OpenRouter"""
        
        niche_context = self._get_niche_design_context(book.sub_niche)
        
        prompt = f"""
You are a professional book cover designer specializing in modern, trending designs for 2024-2025. Create 3 unique, professional cover design concepts for a book titled: "{book.title}"

BOOK CONTEXT:
- Topic: {book.sub_niche.replace('_', ' ').title()}
- Target audience: {niche_context['audience']}
- Industry: {niche_context['industry']}
- Current trends: {', '.join(niche_context['trends'])}

REQUIREMENTS:
- Each design must follow one of these 2024-2025 design trends: glassmorphism, neomorphism, brutalist, organic_shapes, cyberpunk, vintage_modern, minimalist_abstract
- Include specific color palettes (hex codes)
- Suggest typography styles and layouts
- Ensure designs are professional and marketable
- Consider the book's topic for visual metaphors

FORMAT your response as JSON:
[
  {{
    "trend": "trend_name",
    "title": "Design Concept Title",
    "description": "Brief description of the design approach",
    "colors": {{
      "primary": "#hexcode",
      "secondary": "#hexcode", 
      "accent": "#hexcode",
      "background": "#hexcode"
    }},
    "typography": "Font style and hierarchy description",
    "visual_elements": "Key visual elements and layout",
    "mood": "Emotional tone and feeling"
  }},
  {{
    // Second concept
  }},
  {{
    // Third concept  
  }}
]
"""
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://book-generator.com",
                    "X-Title": "Book Cover Generator"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a creative book cover designer who creates modern, professional designs. Always respond with valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.8,
                    "max_tokens": 2000,
                },
                timeout=60
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Track token usage
            if 'usage' in data:
                input_tokens = data['usage'].get('prompt_tokens', 0)
                output_tokens = data['usage'].get('completion_tokens', 0)
                self.usage_tracker.record_usage(input_tokens, output_tokens)
            
            content = data['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                concepts = json.loads(content.strip())
                if isinstance(concepts, list) and len(concepts) >= 3:
                    return concepts[:3]  # Return first 3 concepts
            except json.JSONDecodeError:
                print(f"Failed to parse AI cover concepts JSON: {content}")
            
        except Exception as e:
            print(f"AI cover generation failed: {str(e)}")
        
        # Fallback to predefined concepts if AI fails
        return self._get_fallback_concepts(book.sub_niche)
    
    def _get_niche_design_context(self, sub_niche):
        """Get design context for different niches"""
        contexts = {
            # AI & Digital Transformation
            'ai_productivity_tools': {
                'audience': 'Tech-savvy professionals and entrepreneurs',
                'industry': 'AI productivity software',
                'trends': ['automation', 'efficiency', 'smart technology']
            },
            'digital_nomad_guides': {
                'audience': 'Remote workers and location-independent professionals',
                'industry': 'Digital lifestyle',
                'trends': ['freedom', 'mobility', 'work-life balance']
            },
            'automation_business': {
                'audience': 'Business owners and managers',
                'industry': 'Business process automation',
                'trends': ['efficiency', 'scalability', 'innovation']
            },
            'chatgpt_prompts_mastery': {
                'audience': 'AI enthusiasts and content creators',
                'industry': 'AI prompt engineering',
                'trends': ['artificial intelligence', 'productivity', 'creativity']
            },
            'ai_content_creation': {
                'audience': 'Marketers and content professionals',
                'industry': 'AI content tools',
                'trends': ['automation', 'personalization', 'scale']
            },
            'remote_work_optimization': {
                'audience': 'Remote teams and distributed workers',
                'industry': 'Remote collaboration',
                'trends': ['collaboration', 'productivity', 'wellness']
            },
            
            # Sustainability & Green Tech
            'green_tech_startups': {
                'audience': 'Entrepreneurs and investors',
                'industry': 'Clean technology',
                'trends': ['sustainability', 'innovation', 'impact']
            },
            'sustainable_living': {
                'audience': 'Eco-conscious consumers',
                'industry': 'Sustainable lifestyle',
                'trends': ['environment', 'consciousness', 'wellness']
            },
            'climate_tech': {
                'audience': 'Environmental professionals',
                'industry': 'Climate technology',
                'trends': ['climate action', 'innovation', 'urgency']
            },
            'eco_entrepreneurship': {
                'audience': 'Green entrepreneurs',
                'industry': 'Sustainable business',
                'trends': ['profit', 'purpose', 'sustainability']
            },
            'carbon_footprint_reduction': {
                'audience': 'Businesses and individuals',
                'industry': 'Carbon management',
                'trends': ['climate', 'responsibility', 'action']
            },
            
            # Mental Health Technology
            'digital_detox': {
                'audience': 'Tech users seeking balance',
                'industry': 'Digital wellness',
                'trends': ['mindfulness', 'balance', 'wellness']
            },
            'mindfulness_apps': {
                'audience': 'Mental health seekers',
                'industry': 'Digital therapeutics',
                'trends': ['mindfulness', 'technology', 'healing']
            },
            'mental_health_at_work': {
                'audience': 'HR professionals and employees',
                'industry': 'Workplace wellness',
                'trends': ['mental health', 'workplace', 'support']
            },
            'stress_management_tech': {
                'audience': 'Stressed professionals',
                'industry': 'Stress reduction',
                'trends': ['relaxation', 'technology', 'wellness']
            },
            'sleep_optimization': {
                'audience': 'Health-conscious individuals',
                'industry': 'Sleep technology',
                'trends': ['sleep', 'health', 'optimization']
            },
            
            # Future Skills & Learning
            'prompt_engineering': {
                'audience': 'AI practitioners and developers',
                'industry': 'AI education',
                'trends': ['artificial intelligence', 'skills', 'future']
            },
            'ai_ethics': {
                'audience': 'AI professionals and policymakers',
                'industry': 'AI governance',
                'trends': ['ethics', 'responsibility', 'governance']
            },
            'digital_literacy': {
                'audience': 'All digital users',
                'industry': 'Digital education',
                'trends': ['literacy', 'skills', 'adaptation']
            },
            'remote_collaboration': {
                'audience': 'Remote teams',
                'industry': 'Collaboration technology',
                'trends': ['collaboration', 'remote work', 'efficiency']
            },
            'future_job_skills': {
                'audience': 'Career changers and students',
                'industry': 'Workforce development',
                'trends': ['future', 'skills', 'career']
            },
        }
        
        return contexts.get(sub_niche, {
            'audience': 'Modern professionals',
            'industry': 'Professional development',
            'trends': ['growth', 'success', 'innovation']
        })
    
    def _get_fallback_concepts(self, sub_niche):
        """Fallback concepts if AI generation fails"""
        base_colors = {
            'ai_productivity_tools': {'primary': '#3B82F6', 'secondary': '#1E40AF', 'accent': '#60A5FA', 'background': '#F8FAFC'},
            'digital_nomad_guides': {'primary': '#10B981', 'secondary': '#059669', 'accent': '#34D399', 'background': '#F0FDF4'},
            'automation_business': {'primary': '#8B5CF6', 'secondary': '#7C3AED', 'accent': '#A78BFA', 'background': '#FAF5FF'},
            'sustainable_living': {'primary': '#059669', 'secondary': '#047857', 'accent': '#10B981', 'background': '#ECFDF5'},
            'mental_health_at_work': {'primary': '#7C3AED', 'secondary': '#6D28D9', 'accent': '#8B5CF6', 'background': '#F5F3FF'},
        }
        
        colors = base_colors.get(sub_niche, {'primary': '#3B82F6', 'secondary': '#1E40AF', 'accent': '#60A5FA', 'background': '#F8FAFC'})
        
        return [
            {
                "trend": "glassmorphism",
                "title": "Modern Glass Design",
                "description": "Frosted glass effects with layered transparency",
                "colors": colors,
                "typography": "Clean sans-serif fonts with light weights",
                "visual_elements": "Geometric shapes with subtle shadows",
                "mood": "Modern and professional"
            },
            {
                "trend": "neomorphism",
                "title": "Soft Elevation Design", 
                "description": "Soft shadows creating embedded effects",
                "colors": colors,
                "typography": "Rounded sans-serif with medium contrast",
                "visual_elements": "Soft rounded elements with depth",
                "mood": "Friendly and approachable"
            },
            {
                "trend": "minimalist_abstract",
                "title": "Clean Abstract Design",
                "description": "Minimal geometric shapes with clean lines",
                "colors": colors,
                "typography": "Modern sans-serif hierarchy",
                "visual_elements": "Abstract geometric patterns",
                "mood": "Sophisticated and clean"
            }
        ]
    
    def _create_ai_cover_html(self, title, concept):
        """Create HTML for AI-generated cover design"""
        
        trend = concept.get('trend', 'modern')
        colors = concept.get('colors', {})
        typography = concept.get('typography', 'Modern sans-serif')
        visual_elements = concept.get('visual_elements', 'Clean geometric design')
        
        # Split title for better layout
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        
        # Generate HTML based on trend
        if trend == 'glassmorphism':
            return self._glassmorphism_template(title_line1, title_line2, colors, concept)
        elif trend == 'neomorphism':
            return self._neomorphism_template(title_line1, title_line2, colors, concept)
        elif trend == 'brutalist':
            return self._brutalist_template(title_line1, title_line2, colors, concept)
        elif trend == 'organic_shapes':
            return self._organic_template(title_line1, title_line2, colors, concept)
        elif trend == 'cyberpunk':
            return self._cyberpunk_template(title_line1, title_line2, colors, concept)
        elif trend == 'vintage_modern':
            return self._vintage_modern_template(title_line1, title_line2, colors, concept)
        else:  # minimalist_abstract or default
            return self._minimalist_template(title_line1, title_line2, colors, concept)
    
    def _glassmorphism_template(self, title1, title2, colors, concept):
        """Glassmorphism design with frosted glass effects"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&family=Poppins:wght@300;600&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, {colors.get('background', '#f8fafc')} 0%, {colors.get('primary', '#e2e8f0')} 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    overflow: hidden;
                    font-family: 'Inter', sans-serif;
                }}
                
                .glass-card {{
                    background: rgba(255, 255, 255, 0.25);
                    backdrop-filter: blur(20px);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 24px;
                    padding: 80px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    position: relative;
                    z-index: 10;
                    max-width: 1200px;
                    text-align: center;
                }}
                
                .bg-shape {{
                    position: absolute;
                    width: 600px;
                    height: 600px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 50%;
                    top: -150px;
                    right: -150px;
                    backdrop-filter: blur(40px);
                }}
                
                .bg-shape-2 {{
                    position: absolute;
                    width: 400px;
                    height: 400px;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 30%;
                    bottom: -100px;
                    left: -100px;
                    transform: rotate(45deg);
                    backdrop-filter: blur(30px);
                }}
                
                .title {{
                    font-family: 'Poppins', sans-serif;
                    font-size: 120px;
                    font-weight: 700;
                    line-height: 1.1;
                    margin-bottom: 40px;
                    color: {colors.get('primary', '#1a365d')};
                    text-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    letter-spacing: -2px;
                }}
                
                .title-line-2 {{
                    font-size: 80px;
                    font-weight: 600;
                    margin-top: 20px;
                }}
                
                .subtitle {{
                    font-size: 32px;
                    font-weight: 300;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    color: {colors.get('secondary', '#4a5568')};
                    opacity: 0.8;
                    margin-top: 40px;
                }}
                
                .accent-element {{
                    width: 150px;
                    height: 4px;
                    background: linear-gradient(90deg, {colors.get('accent', '#3b82f6')}, transparent);
                    margin: 40px auto 0;
                    border-radius: 2px;
                }}
            </style>
        </head>
        <body>
            <div class="bg-shape"></div>
            <div class="bg-shape-2"></div>
            <div class="glass-card">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Professional Guide</div>
                <div class="accent-element"></div>
            </div>
        </body>
        </html>
        """
    
    def _neomorphism_template(self, title1, title2, colors, concept):
        """Neomorphism design with soft shadows"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;600;800&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: {colors.get('background', '#f1f5f9')};
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    font-family: 'Nunito', sans-serif;
                }}
                
                .neo-card {{
                    background: {colors.get('background', '#f1f5f9')};
                    border-radius: 32px;
                    padding: 100px;
                    box-shadow: 
                        20px 20px 40px rgba(0,0,0,0.1),
                        -20px -20px 40px rgba(255,255,255,0.8);
                    position: relative;
                    z-index: 10;
                    max-width: 1200px;
                    text-align: center;
                }}
                
                .inner-shadow {{
                    position: absolute;
                    top: 40px;
                    left: 40px;
                    right: 40px;
                    bottom: 40px;
                    border-radius: 24px;
                    box-shadow: 
                        inset 10px 10px 20px rgba(0,0,0,0.1),
                        inset -10px -10px 20px rgba(255,255,255,0.8);
                }}
                
                .title {{
                    font-size: 110px;
                    font-weight: 800;
                    line-height: 1.1;
                    margin-bottom: 30px;
                    color: {colors.get('primary', '#2d3748')};
                    letter-spacing: -1px;
                    position: relative;
                    z-index: 20;
                }}
                
                .title-line-2 {{
                    font-size: 75px;
                    font-weight: 600;
                    margin-top: 15px;
                }}
                
                .subtitle {{
                    font-size: 28px;
                    font-weight: 300;
                    letter-spacing: 6px;
                    text-transform: uppercase;
                    color: {colors.get('secondary', '#4a5568')};
                    margin-top: 30px;
                    position: relative;
                    z-index: 20;
                }}
                
                .accent-dot {{
                    width: 12px;
                    height: 12px;
                    background: {colors.get('accent', '#3b82f6')};
                    border-radius: 50%;
                    margin: 30px auto 0;
                    box-shadow: 
                        4px 4px 8px rgba(0,0,0,0.2),
                        -4px -4px 8px rgba(255,255,255,0.8);
                }}
            </style>
        </head>
        <body>
            <div class="neo-card">
                <div class="inner-shadow"></div>
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Complete Guide</div>
                <div class="accent-dot"></div>
            </div>
        </body>
        </html>
        """
    
    def _minimalist_template(self, title1, title2, colors, concept):
        """Minimalist abstract design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600;900&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: {colors.get('background', '#ffffff')};
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    font-family: 'Inter', sans-serif;
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    max-width: 1200px;
                }}
                
                .geometric-bg {{
                    position: absolute;
                    width: 800px;
                    height: 800px;
                    background: linear-gradient(45deg, {colors.get('primary', '#3b82f6')}20, {colors.get('accent', '#60a5fa')}20);
                    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
                    top: -200px;
                    right: -200px;
                    opacity: 0.1;
                }}
                
                .title {{
                    font-size: 140px;
                    font-weight: 900;
                    line-height: 1.1;
                    margin-bottom: 40px;
                    color: {colors.get('primary', '#1a365d')};
                    letter-spacing: -3px;
                }}
                
                .title-line-2 {{
                    font-size: 100px;
                    font-weight: 600;
                    margin-top: 20px;
                }}
                
                .subtitle {{
                    font-size: 36px;
                    font-weight: 300;
                    letter-spacing: 12px;
                    text-transform: uppercase;
                    color: {colors.get('secondary', '#4a5568')};
                    margin-top: 40px;
                }}
                
                .minimal-line {{
                    width: 300px;
                    height: 3px;
                    background: {colors.get('accent', '#3b82f6')};
                    margin: 40px auto 0;
                }}
            </style>
        </head>
        <body>
            <div class="geometric-bg"></div>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Master Guide</div>
                <div class="minimal-line"></div>
            </div>
        </body>
        </html>
        """
    
    def _brutalist_template(self, title1, title2, colors, concept):
        """Brutalist design with bold typography"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;600;800&family=Bebas+Neue&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: {colors.get('primary', '#000000')};
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    font-family: 'Oswald', sans-serif;
                }}
                
                .brutal-border {{
                    position: absolute;
                    top: 100px;
                    left: 100px;
                    right: 100px;
                    bottom: 100px;
                    border: 8px solid {colors.get('accent', '#ffffff')};
                    z-index: 5;
                }}
                
                .content {{
                    background: {colors.get('secondary', '#ffffff')};
                    padding: 80px;
                    position: relative;
                    z-index: 10;
                    max-width: 1200px;
                    text-align: center;
                    box-shadow: 20px 20px 0px {colors.get('accent', '#dc2626')};
                }}
                
                .title {{
                    font-family: 'Bebas Neue', sans-serif;
                    font-size: 160px;
                    line-height: 0.9;
                    margin-bottom: 30px;
                    color: {colors.get('primary', '#000000')};
                    text-transform: uppercase;
                    letter-spacing: 4px;
                }}
                
                .title-line-2 {{
                    font-size: 120px;
                    margin-top: 10px;
                }}
                
                .subtitle {{
                    font-size: 48px;
                    font-weight: 800;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    color: {colors.get('accent', '#dc2626')};
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="brutal-border"></div>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">GUIDE</div>
            </div>
        </body>
        </html>
        """
    
    def _organic_template(self, title1, title2, colors, concept):
        """Organic shapes design"""
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
                    background: linear-gradient(135deg, {colors.get('background', '#f0fdf4')} 0%, {colors.get('primary', '#10b981')} 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    font-family: 'Lato', sans-serif;
                }}
                
                .organic-shape {{
                    position: absolute;
                    width: 700px;
                    height: 700px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
                    top: -150px;
                    right: -150px;
                    backdrop-filter: blur(20px);
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    max-width: 1100px;
                }}
                
                .title {{
                    font-family: 'Playfair Display', serif;
                    font-size: 130px;
                    font-weight: 900;
                    line-height: 1.1;
                    margin-bottom: 40px;
                    color: {colors.get('secondary', '#047857')};
                    letter-spacing: -2px;
                }}
                
                .title-line-2 {{
                    font-size: 90px;
                    font-weight: 700;
                    margin-top: 20px;
                }}
                
                .subtitle {{
                    font-size: 34px;
                    font-weight: 300;
                    letter-spacing: 10px;
                    text-transform: uppercase;
                    color: {colors.get('accent', '#059669')};
                    margin-top: 40px;
                }}
                
                .organic-accent {{
                    width: 200px;
                    height: 8px;
                    background: linear-gradient(90deg, {colors.get('accent', '#10b981')}, {colors.get('primary', '#059669')});
                    margin: 40px auto 0;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="organic-shape"></div>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Natural Guide</div>
                <div class="organic-accent"></div>
            </div>
        </body>
        </html>
        """
    
    def _cyberpunk_template(self, title1, title2, colors, concept):
        """Cyberpunk design with neon effects"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;600;800&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, {colors.get('primary', '#000000')} 0%, {colors.get('secondary', '#1f2937')} 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    font-family: 'Rajdhani', sans-serif;
                    overflow: hidden;
                }}
                
                .cyber-grid {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-image: 
                        linear-gradient(rgba(139, 92, 246, 0.1) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(139, 92, 246, 0.1) 1px, transparent 1px);
                    background-size: 50px 50px;
                }}
                
                .neon-glow {{
                    position: absolute;
                    width: 600px;
                    height: 600px;
                    background: radial-gradient(circle, {colors.get('accent', '#ec4899')}40 0%, transparent 70%);
                    top: -100px;
                    right: -100px;
                    filter: blur(50px);
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    max-width: 1200px;
                }}
                
                .title {{
                    font-size: 140px;
                    font-weight: 800;
                    line-height: 1.1;
                    margin-bottom: 40px;
                    color: {colors.get('accent', '#ec4899')};
                    text-shadow: 
                        0 0 20px {colors.get('accent', '#ec4899')},
                        0 0 40px {colors.get('accent', '#ec4899')},
                        0 0 60px {colors.get('accent', '#ec4899')};
                    letter-spacing: -2px;
                    text-transform: uppercase;
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
                    color: {colors.get('secondary', '#8b5cf6')};
                    margin-top: 40px;
                    text-shadow: 0 0 10px {colors.get('secondary', '#8b5cf6')};
                }}
                
                .cyber-line {{
                    width: 250px;
                    height: 2px;
                    background: linear-gradient(90deg, transparent, {colors.get('accent', '#ec4899')}, transparent);
                    margin: 40px auto 0;
                    position: relative;
                }}
                
                .cyber-line::before {{
                    content: '';
                    position: absolute;
                    top: -2px;
                    left: 0;
                    right: 0;
                    height: 6px;
                    background: linear-gradient(90deg, transparent, {colors.get('accent', '#ec4899')}40, transparent);
                    filter: blur(2px);
                }}
            </style>
        </head>
        <body>
            <div class="cyber-grid"></div>
            <div class="neon-glow"></div>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Future Guide</div>
                <div class="cyber-line"></div>
            </div>
        </body>
        </html>
        """
    
    def _vintage_modern_template(self, title1, title2, colors, concept):
        """Vintage modern design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Poppins:wght@300;600&display=swap');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, {colors.get('background', '#fef3c7')} 0%, {colors.get('primary', '#f59e0b')} 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    position: relative;
                    font-family: 'Poppins', sans-serif;
                }}
                
                .vintage-border {{
                    position: absolute;
                    top: 80px;
                    left: 80px;
                    right: 80px;
                    bottom: 80px;
                    border: 6px solid {colors.get('secondary', '#d97706')};
                    border-radius: 20px;
                    opacity: 0.3;
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    max-width: 1100px;
                    background: rgba(255, 255, 255, 0.9);
                    padding: 80px;
                    border-radius: 16px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }}
                
                .title {{
                    font-family: 'Crimson Text', serif;
                    font-size: 120px;
                    font-weight: 600;
                    line-height: 1.1;
                    margin-bottom: 40px;
                    color: {colors.get('secondary', '#92400e')};
                    letter-spacing: -1px;
                }}
                
                .title-line-2 {{
                    font-size: 85px;
                    font-weight: 400;
                    margin-top: 20px;
                }}
                
                .subtitle {{
                    font-size: 32px;
                    font-weight: 300;
                    letter-spacing: 6px;
                    text-transform: uppercase;
                    color: {colors.get('accent', '#f59e0b')};
                    margin-top: 40px;
                }}
                
                .vintage-accent {{
                    width: 180px;
                    height: 4px;
                    background: linear-gradient(90deg, {colors.get('secondary', '#d97706')}, {colors.get('accent', '#f59e0b')});
                    margin: 40px auto 0;
                    border-radius: 2px;
                    position: relative;
                }}
                
                .vintage-accent::before {{
                    content: '';
                    position: absolute;
                    width: 8px;
                    height: 8px;
                    background: {colors.get('secondary', '#d97706')};
                    border-radius: 50%;
                    left: -4px;
                    top: -2px;
                }}
                
                .vintage-accent::after {{
                    content: '';
                    position: absolute;
                    width: 8px;
                    height: 8px;
                    background: {colors.get('secondary', '#d97706')};
                    border-radius: 50%;
                    right: -4px;
                    top: -2px;
                }}
            </style>
        </head>
        <body>
            <div class="vintage-border"></div>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Timeless Guide</div>
                <div class="vintage-accent"></div>
            </div>
        </body>
        </html>
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
