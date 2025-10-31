"""
Professional AI Cover Generator using OpenRouter DeepSeek R1T2 Chimera
Generates comprehensive graphical covers using ReportLab with AI prompts
"""

import os
import json
import requests
import random
import time
from pathlib import Path
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle as MPLCircle
import io
from datetime import datetime
import textwrap
from PIL import Image as PILImage, ImageDraw
from books.services.usage_tracker import UsageTracker
from books.services.trending import get_trending_context
from covers.layout_engine import CoverLayoutEngine
from covers.template_library import resolve_template


# Professional Cover Prompt for ReportLab
REPORTLAB_COVER_PROMPT = """
You are a senior ReportLab graphics designer specializing in creating professional PDF book covers. Generate 3 distinct, comprehensive cover design prompts that use ReportLab's canvas and graphics capabilities.

Book Details:
Title: "{title}"
Audience: {audience}
Niche: "{sub_niche}"
Trending Context: {trending_info}

Requirements for Each Cover:
1. **Use ReportLab canvas.drawString(), canvas.setFont(), canvas.setFillColor()** for text rendering
2. **Include the ACTUAL BOOK TITLE "{title}"** prominently on each cover
3. **Use professional color schemes** with HexColor() for backgrounds and text
4. **Create visual elements** using Drawing, Rect, Circle, Line, Polygon from reportlab.graphics.shapes
5. **Implement layout techniques** like centered positioning, geometric backgrounds, gradient effects
6. **Add graphical diagrams** using matplotlib integration for charts, patterns, or abstract designs
7. **Ensure accessibility** with high contrast ratios and readable fonts

Design Trends (use 3 different ones):
1. **Geometric Modern**: Rectangles, circles, lines, grids - clean and structured
2. **Organic Flow**: Curves, waves, natural shapes - fluid and dynamic  
3. **Typography Focus**: Large text with subtle background elements - text-driven design
4. **Data Visualization**: Charts, graphs, patterns - information-rich design
5. **Abstract Art**: Custom shapes, gradients, artistic elements - creative and bold
6. **Professional Minimal**: Simple layouts, ample white space - clean and elegant
7. **Tech Futuristic**: Digital elements, neon effects, modern patterns - cutting-edge

For Each Design Direction, Provide:
1. **trend**: One of the above trend names (lowercase, underscores instead of spaces)
2. **concept_name**: Short catchy name for this design direction
3. **reportlab_code**: Complete Python code using ReportLab to create the cover
4. **matplotlib_elements**: Optional matplotlib code for advanced graphics
5. **colors**: Primary, secondary, accent, background hex codes
6. **layout_description**: How elements are positioned and layered
7. **accessibility_notes**: Contrast and readability considerations

FORMAT your response as VALID JSON only:
{{
  "designs": [
    {{
      "trend": "geometric_modern",
      "concept_name": "Structured Excellence",
      "reportlab_code": "Complete ReportLab Python code here...",
      "matplotlib_elements": "Optional matplotlib code...",
      "colors": {{
        "primary": "#1a365d",
        "secondary": "#4a5568", 
        "accent": "#3b82f6",
        "background": "#ffffff"
      }},
      "layout_description": "Centered title with geometric background grid",
      "accessibility_notes": "High contrast text on light background"
    }},
    ... 2 more unique designs
  ]
}}

Remember:
- Use the REAL book title "{title}" in all designs
- Provide EXECUTABLE ReportLab Python code
- Make each design visually distinct
- Ensure professional quality for book sales
- Return ONLY valid JSON, no extra text
"""


# Professional Cover Prompt
PROFESSIONAL_COVER_PROMPT = """
You are a senior book cover art director specializing in modern, trending 2025-2027 design aesthetics. Generate 3 distinct, professional cover design directions based on the following book metadata:

Title: "{title}"
Subtitle: "{subtitle}"
Audience: {audience}
Niche: "{sub_niche}"
Trending Context: {trending_info}

Requirements:
- Each design must be VISUALLY DISTINCT and follow different 2025-2027 design trends
- Use the ACTUAL BOOK TITLE "{title}" in all designs - NO PLACEHOLDERS
- Designs should reflect the book's specific topic and audience
- Modern, professional, and marketable for digital publishing

Design Trends to Choose From (use 3 different ones):
1. **Glass morphism** - Frosted glass effects, transparency layers, soft shadows, light backgrounds
2. **Neomorphism** - Soft embossed/debossed effects, subtle shadows, monochromatic with depth
3. **Brutalist** - Bold typography, high contrast, raw edges, geometric blocks, striking colors
4. **Organic Shapes** - Flowing curves, natural forms, earthy palettes, fluid layouts
5. **Cyberpunk/Futuristic** - Neon accents, dark themes, tech elements, grid patterns, vibrant highlights
6. **Minimalist Abstract** - Clean geometric shapes, negative space, limited palette, strong typography
7. **Vintage Modern** - Retro color palettes, contemporary typography, nostalgic with modern twist

For Each Design Direction, Provide:
1. **trend**: One of the above trend names (lowercase, underscores instead of spaces)
2. **concept_name**: Short catchy name for this design direction
3. **description**: 2-3 sentences describing the visual approach
4. **colors**: Object with primary, secondary, accent, background (hex codes)
5. **typography**: Font family suggestions and hierarchy (title/subtitle sizing)
6. **visual_elements**: Specific shapes, patterns, or motifs to include
7. **mood**: Emotional tone (professional, energetic, calm, bold, etc.)
8. **layout**: Description of text placement and visual balance
9. **accessibility**: Contrast ratio notes and readability considerations

FORMAT your response as VALID JSON only (no other text):
{{
  "designs": [
    {{
      "trend": "glassmorphism",
      "concept_name": "Transparent Innovation",
      "description": "Clean frosted glass panels with subtle blur effects...",
      "colors": {{
        "primary": "#3B82F6",
        "secondary": "#1E40AF",
        "accent": "#60A5FA",
        "background": "#F8FAFC"
      }},
      "typography": "Large bold sans-serif title (120pt), light weight subtitle (36pt)",
      "visual_elements": "Overlapping translucent geometric shapes, soft drop shadows",
      "mood": "Modern, professional, tech-forward",
      "layout": "Centered title with geometric background elements, subtitle at bottom",
      "accessibility": "High contrast text on light background, AAA compliant"
    }},
    ... 2 more unique designs
  ]
}}

Remember:
- Use the REAL book title "{title}" in your descriptions
- Make each design visually distinct (different trends, colors, layouts)
- Ensure professional quality suitable for digital book sales
- Return ONLY valid JSON, no markdown code blocks or extra text
"""


class CoverGeneratorProfessional:
    """
    Professional AI cover generator using ReportLab with comprehensive graphical designs
    Uses Cloudflare AI for design concepts (NO OpenRouter)
    """
    
    def __init__(self):
        # Use Cloudflare AI instead of OpenRouter
        from customllm.services.cloudflare_client import CloudflareAIClient
        try:
            self.cloudflare_client = CloudflareAIClient()
        except Exception as e:
            print(f"⚠️  Cloudflare AI not available, will use fallback designs: {e}")
            self.cloudflare_client = None
        
        self.usage_tracker = UsageTracker()
        self.media_root = Path(settings.MEDIA_ROOT)
        self.covers_dir = self.media_root / 'covers'
        self.covers_dir.mkdir(parents=True, exist_ok=True)

    # --- Contrast utilities ---
    def _hex_to_rgb(self, hex_color: str):
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

    def _luminance(self, rgb):
        def f(c):
            return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
        r, g, b = rgb
        return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)

    def _contrast_ratio(self, c1: str, c2: str) -> float:
        try:
            L1 = self._luminance(self._hex_to_rgb(c1))
            L2 = self._luminance(self._hex_to_rgb(c2))
            L1, L2 = (L1, L2) if L1 >= L2 else (L2, L1)
            return (L1 + 0.05) / (L2 + 0.05)
        except Exception:
            return 1.0

    def _ensure_contrast(self, colors: dict) -> dict:
        # Enforce minimum 4.5:1 contrast between primary text and background
        primary = colors.get('primary', '#1a365d')
        background = colors.get('background', '#ffffff')
        if self._contrast_ratio(primary, background) < 4.5:
            # If low contrast, force primary to dark or light depending on bg
            bg_lum = self._luminance(self._hex_to_rgb(background))
            colors['primary'] = '#0a0a0a' if bg_lum > 0.5 else '#ffffff'
        return colors
    
    def _create_grid_overlay(self, image_abs_path: str):
        """Create a rule-of-thirds grid overlay PNG next to the cover image for review.
        Saves as <name>_grid.png in the same directory.
        """
        try:
            if not os.path.exists(image_abs_path):
                return
            img = PILImage.open(image_abs_path).convert("RGBA")
            w, h = img.size
            overlay = PILImage.new("RGBA", (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            # Rule of thirds positions
            v1 = w // 3
            v2 = 2 * w // 3
            h1 = h // 3
            h2 = 2 * h // 3
            line_color = (255, 255, 255, 90)
            # Vertical lines
            draw.line([(v1, 0), (v1, h)], fill=line_color, width=3)
            draw.line([(v2, 0), (v2, h)], fill=line_color, width=3)
            # Horizontal lines
            draw.line([(0, h1), (w, h1)], fill=line_color, width=3)
            draw.line([(0, h2), (w, h2)], fill=line_color, width=3)
            # Merge and save
            out = PILImage.alpha_composite(img, overlay)
            base, ext = os.path.splitext(image_abs_path)
            out_path = f"{base}_grid.png"
            out.convert("RGB").save(out_path, "PNG")
        except Exception:
            # Non-fatal
            pass

    def _create_golden_ratio_overlay(self, image_abs_path: str):
        """Create a golden-ratio guide overlay PNG (0.382 / 0.618 lines).
        Saves as <name>_golden.png.
        """
        try:
            if not os.path.exists(image_abs_path):
                return
            img = PILImage.open(image_abs_path).convert("RGBA")
            w, h = img.size
            overlay = PILImage.new("RGBA", (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            # Golden sections
            x1 = int(w * 0.382)
            x2 = int(w * 0.618)
            y1 = int(h * 0.382)
            y2 = int(h * 0.618)
            line_color = (255, 215, 0, 90)  # golden tint
            # Vertical golden lines
            draw.line([(x1, 0), (x1, h)], fill=line_color, width=3)
            draw.line([(x2, 0), (x2, h)], fill=line_color, width=3)
            # Horizontal golden lines
            draw.line([(0, y1), (w, y1)], fill=line_color, width=3)
            draw.line([(0, y2), (w, y2)], fill=line_color, width=3)
            out = PILImage.alpha_composite(img, overlay)
            base, ext = os.path.splitext(image_abs_path)
            out_path = f"{base}_golden.png"
            out.convert("RGB").save(out_path, "PNG")
        except Exception:
            pass

    def _save_cover_metadata(self, cover_obj, concept: dict):
        """Persist cover generation metadata alongside the image (JSON file)."""
        try:
            # Resolve absolute image path
            rel_image = cover_obj.image_path  # e.g., "covers/<file>.png"
            image_abs = os.path.join(self.media_root, rel_image)
            # Gather basic info
            dims = None
            try:
                with PILImage.open(image_abs) as im:
                    dims = {"width": im.width, "height": im.height}
            except Exception:
                dims = None
            # Contrast ratio if colors present
            colors_obj = (concept or {}).get('colors', {})
            primary = colors_obj.get('primary')
            background = colors_obj.get('background')
            contrast = None
            if primary and background:
                contrast = round(self._contrast_ratio(primary, background), 2)

            payload = {
                "cover_id": cover_obj.id,
                "book_id": cover_obj.book_id,
                "template_style": cover_obj.template_style,
                "image": rel_image,
                "pdf": cover_obj.pdf_path,
                "dimensions": dims,
                "contrast_primary_vs_background": contrast,
                "concept": concept,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

            # Save next to image as .metadata.json
            base, _ = os.path.splitext(image_abs)
            meta_path = f"{base}.metadata.json"
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception:
            # Non-fatal
            pass
    
    def generate_three_covers(self, book):
        """
        Generate 3 AI-powered ReportLab covers for a book
        Each cover includes the book title and comprehensive graphical elements
        """
        from covers.models import Cover
        
        print(f"\n=== Generating AI ReportLab Covers for Book: {book.title} ===")
        print(f"Sub-niche: {book.niche.name}")
        print(f"Audience: {self._infer_audience(book.niche.name)}")
        
        covers = []
        
        # Generate AI ReportLab design concepts
        try:
            design_concepts = self._generate_ai_reportlab_concepts(book)
            
            if not design_concepts or len(design_concepts) < 3:
                raise Exception("Failed to generate 3 ReportLab design concepts from AI")
            
            print(f"Successfully generated {len(design_concepts)} AI ReportLab design concepts")
            
        except Exception as e:
            print(f"AI ReportLab generation failed: {str(e)}")
            raise Exception(f"Cover generation failed: {str(e)}")
        
        # Create covers from AI ReportLab concepts
        for i, concept in enumerate(design_concepts[:3]):  # Ensure exactly 3
            try:
                print(f"\nCreating cover {i+1}/3: {concept.get('concept_name', 'Design')}")
                
                # Generate unique filename
                clean_title = self._clean_filename(book.title)
                filename = f"{clean_title}_cover_{i+1}_{random.randint(1000, 9999)}"
                pdf_path = self.covers_dir / f"{filename}.pdf"
                png_path = self.covers_dir / f"{filename}.png"
                
                # Create ReportLab PDF using AI-generated code
                self._create_reportlab_cover_pdf(book, concept, str(pdf_path))
                
                # Convert PDF to PNG for preview
                self._pdf_to_png(str(pdf_path), str(png_path))
                
                # Create Cover object
                cover = Cover.objects.create(
                    book=book,
                    template_style=f"ai_reportlab_{concept.get('trend', 'modern')}_{i+1}",
                    image_path=f"covers/{png_path.name}",
                    pdf_path=f"covers/{pdf_path.name}",
                    generation_params={
                        'ai_generated': True,
                        'design_concept': concept.get('concept_name', 'Professional Design'),
                        'trend_style': concept.get('trend', 'modern'),
                        'colors': concept.get('colors', {}),
                        'reportlab_code': concept.get('reportlab_code', ''),
                        'matplotlib_elements': concept.get('matplotlib_elements', ''),
                        'layout_description': concept.get('layout_description', ''),
                        'accessibility_notes': concept.get('accessibility_notes', ''),
                    }
                )
                # Store metadata and a grid overlay for review
                try:
                    self._save_cover_metadata(cover, concept)
                finally:
                    self._create_grid_overlay(str(png_path))
                    self._create_golden_ratio_overlay(str(png_path))
                covers.append(cover)
                print(f"✓ Cover {i+1} created successfully")
                
            except Exception as e:
                print(f"✗ Cover {i+1} creation failed: {str(e)}")
                # Continue to try next cover instead of failing completely
                continue
        
        if len(covers) == 0:
            raise Exception("Failed to create any covers")
        
        print(f"\n=== Successfully generated {len(covers)} ReportLab covers ===\n")
        return covers
    
    def generate_cover_prompts(self, book) -> list:
        """
        Generate 3 ReportLab cover design prompts for a book
        Returns text prompts describing how to render covers using ReportLab
        """
        print(f"\n=== Generating ReportLab Cover Prompts for Book: {book.title} ===")
        
        try:
            # Generate AI cover concepts
            design_concepts = self._generate_ai_cover_concepts(book)
            
            if not design_concepts or len(design_concepts) < 3:
                raise Exception("Failed to generate 3 design concepts from AI")
            
            print(f"Successfully generated {len(design_concepts)} AI design concepts")
            
            # Convert AI concepts to ReportLab prompts
            prompts = []
            for i, concept in enumerate(design_concepts[:3]):
                prompt = self._convert_concept_to_reportlab_prompt(book.title, concept, i+1)
                prompts.append(prompt)
            
            return prompts
            
        except Exception as e:
            print(f"Cover prompt generation failed: {str(e)}")
            # Return fallback prompts
            return self._get_fallback_reportlab_prompts(book.title)
    
    def _convert_concept_to_reportlab_prompt(self, title: str, concept: dict, cover_number: int) -> str:
        """Convert AI design concept to ReportLab rendering prompt"""
        
        trend = concept.get('trend', 'minimalist')
        colors = concept.get('colors', {})
        typography = concept.get('typography', 'Large bold sans-serif title')
        visual_elements = concept.get('visual_elements', 'Simple geometric shapes')
        layout = concept.get('layout', 'Centered title')
        
        # Split title for better layout
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        
        prompt = f"""Cover {cover_number}: {concept.get('concept_name', 'Professional Design')}

Use ReportLab to create a {trend} style cover for the book "{title}".

Canvas Setup:
- Page size: letter (8.5 x 11 inches)
- Background color: {colors.get('background', '#FFFFFF')}

Title Rendering:
- Primary title: "{title_line1}"
{f'- Secondary title: "{title_line2}"' if title_line2 else ''}
- Font: Helvetica-Bold
- Size: 48pt for primary, 32pt for secondary
- Color: {colors.get('primary', '#000000')}
- Position: Centered horizontally, vertically centered
- Line spacing: 1.2

Visual Elements:
- Style: {trend}
- Colors: Primary {colors.get('primary', '#000000')}, Secondary {colors.get('secondary', '#666666')}, Accent {colors.get('accent', '#999999')}
- Elements: {visual_elements}

Layout Instructions:
{layout}

ReportLab Code Structure:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

def create_cover{cover_number}(c):
    # Set up canvas
    c.setPageSize(letter)
    
    # Background
    c.setFillColor(HexColor('{colors.get('background', '#FFFFFF')}'))
    c.rect(0, 0, 8.5*inch, 11*inch, fill=1)
    
    # Title rendering
    c.setFillColor(HexColor('{colors.get('primary', '#000000')}'))
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(4.25*inch, 6*inch, "{title_line1}")
    {f'c.drawCentredString(4.25*inch, 5.5*inch, "{title_line2}")' if title_line2 else ''}
    
    # Add visual elements based on {trend} style
    # {visual_elements}
```

Accessibility: Ensure high contrast ratio between text and background colors."""
        
        return prompt
    
    def _get_fallback_reportlab_prompts(self, title: str) -> list:
        """Return fallback ReportLab prompts if AI generation fails"""
        
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        cover_a_lines = [
            "Cover A: Modern Minimalist",
            "",
            f'Use ReportLab to create a clean, modern cover for "{title}".',
            "",
            "Canvas Setup:",
            "- Page size: letter (8.5 x 11 inches)",
            "- Background: White (#FFFFFF)",
            "",
            "Title Rendering:",
            f'- Primary title: "{title_line1}"',
        ]
        if title_line2:
            cover_a_lines.append(f'- Secondary title: "{title_line2}"')
        cover_a_lines.extend([
            "- Font: Helvetica-Bold, 48pt primary, 32pt secondary",
            "- Color: Navy blue (#1a365d)",
            "- Position: Centered",
            "",
            "Visual Elements:",
            "- Add a simple colored rectangle background",
            "- Use HexColor('#e2e8f0') for background shape",
            "",
            "ReportLab Code:",
            "```python",
            "from reportlab.lib.pagesizes import letter",
            "from reportlab.pdfgen import canvas",
            "from reportlab.lib.colors import HexColor",
            "",
            "def create_coverA(c):",
            "    c.setPageSize(letter)",
            "    c.setFillColor(HexColor('#e2e8f0'))",
            "    c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10*inch, fill=1)",
            "    c.setFillColor(HexColor('#1a365d'))",
            '    c.setFont("Helvetica-Bold", 48)',
            f'    c.drawCentredString(4.25*inch, 6*inch, "{title_line1}")',
        ])
        if title_line2:
            cover_a_lines.append(f'    c.drawCentredString(4.25*inch, 5.5*inch, "{title_line2}")')
        cover_a_lines.append("```")

        cover_b_lines = [
            "Cover B: Elegant Typography",
            "",
            f'Use ReportLab to create an elegant typographic cover for "{title}".',
            "",
            "Canvas Setup:",
            "- Page size: letter",
            "- Background: Light gray gradient (#f8fafc to #e2e8f0)",
            "",
            "Title Rendering:",
            f'- Primary title: "{title_line1}"',
        ]
        if title_line2:
            cover_b_lines.append(f'- Secondary title: "{title_line2}"')
        cover_b_lines.extend([
            "- Font: Helvetica-Bold, 52pt primary, 36pt secondary",
            "- Color: Dark blue (#2d3748)",
            "- Position: Left-aligned with margin",
            "",
            "Visual Elements:",
            "- Add decorative line under title",
            "- Use subtle background pattern",
            "",
            "ReportLab Code:",
            "```python",
            "from reportlab.lib.pagesizes import letter",
            "from reportlab.pdfgen import canvas",
            "from reportlab.lib.colors import HexColor",
            "",
            "def create_coverB(c):",
            "    c.setPageSize(letter)",
            "    # Gradient background simulation",
            "    c.setFillColor(HexColor('#f8fafc'))",
            "    c.rect(0, 0, 8.5*inch, 11*inch, fill=1)",
            "    c.setFillColor(HexColor('#2d3748'))",
            '    c.setFont("Helvetica-Bold", 52)',
            f'    c.drawString(1*inch, 7*inch, "{title_line1}")',
        ])
        if title_line2:
            cover_b_lines.extend([
                '    c.setFont("Helvetica-Bold", 36)',
                f'    c.drawString(1*inch, 6.5*inch, "{title_line2}")',
            ])
        cover_b_lines.extend([
            "    # Decorative line",
            "    c.setStrokeColor(HexColor('#4a5568'))",
            "    c.setLineWidth(3)",
            "    c.line(1*inch, 6*inch, 7.5*inch, 6*inch)",
            "```",
        ])

        cover_c_lines = [
            "Cover C: Bold Statement",
            "",
            f'Use ReportLab to create a bold, striking cover for "{title}".',
            "",
            "Canvas Setup:",
            "- Page size: letter",
            "- Background: Dark with light text (#1a202c)",
            "",
            "Title Rendering:",
            f'- Primary title: "{title_line1}"',
        ]
        if title_line2:
            cover_c_lines.append(f'- Secondary title: "{title_line2}"')
        cover_c_lines.extend([
            "- Font: Helvetica-Bold, 56pt primary, 40pt secondary",
            "- Color: White (#ffffff)",
            "- Position: Centered",
            "",
            "Visual Elements:",
            "- High contrast design",
            "- Bold background shapes",
            "",
            "ReportLab Code:",
            "```python",
            "from reportlab.lib.pagesizes import letter",
            "from reportlab.pdfgen import canvas",
            "from reportlab.lib.colors import HexColor",
            "",
            "def create_coverC(c):",
            "    c.setPageSize(letter)",
            "    c.setFillColor(HexColor('#1a202c'))",
            "    c.rect(0, 0, 8.5*inch, 11*inch, fill=1)",
            "    c.setFillColor(HexColor('#ffffff'))",
            '    c.setFont("Helvetica-Bold", 56)',
            f'    c.drawCentredString(4.25*inch, 6*inch, "{title_line1}")',
        ])
        if title_line2:
            cover_c_lines.extend([
                '    c.setFont("Helvetica-Bold", 40)',
                f'    c.drawCentredString(4.25*inch, 5.5*inch, "{title_line2}")',
            ])
        cover_c_lines.append("```")

        return [
            "\n".join(cover_a_lines),
            "\n".join(cover_b_lines),
            "\n".join(cover_c_lines),
        ]
        """
        Generate 3 AI-powered cover designs for a book
        NO FALLBACK TEMPLATES - All designs are AI-generated
        """
        from covers.models import Cover
        
        print(f"\n=== Generating AI Covers for Book: {book.title} ===")
        print(f"Sub-niche: {book.niche.name}")
        print(f"Audience: {self._infer_audience(book.niche.name)}")
        
        covers = []
        
        # Generate AI ReportLab design concepts
        try:
            design_concepts = self._generate_ai_reportlab_concepts(book)
            
            if not design_concepts or len(design_concepts) < 3:
                raise Exception("Failed to generate 3 design concepts from AI")
            
            print(f"Successfully generated {len(design_concepts)} AI design concepts")
            
        except Exception as e:
            print(f"AI cover generation failed: {str(e)}")
            raise Exception(f"Cover generation failed: {str(e)}")
        
        # Create covers from AI concepts
        for i, concept in enumerate(design_concepts[:3]):  # Ensure exactly 3
            try:
                print(f"\nCreating cover {i+1}/3: {concept.get('concept_name', 'Design')}")
                
                # Generate unique filename
                clean_title = self._clean_filename(book.title)
                filename = f"{clean_title}_cover_{i+1}_{random.randint(1000, 9999)}"
                image_path = self.covers_dir / f"{filename}.png"
                pdf_path = self.covers_dir / f"{filename}.pdf"
                
                # Create HTML with AI-generated design
                html_content = self._create_ai_cover_html(book.title, concept)
                
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
                    template_style=f"ai_{concept.get('trend', 'modern')}_{i+1}",
                    image_path=f"covers/{image_path.name}",
                    pdf_path=f"covers/{pdf_path.name}",
                    generation_params={
                        'ai_generated': True,
                        'design_concept': concept.get('concept_name', 'Professional Design'),
                        'trend_style': concept.get('trend', 'modern'),
                        'colors': concept.get('colors', {}),
                        'mood': concept.get('mood', 'professional'),
                    }
                )
                covers.append(cover)
                print(f"✓ Cover {i+1} created successfully")
                
            except Exception as e:
                print(f"✗ Cover {i+1} creation failed: {str(e)}")
                # Continue to try next cover instead of failing completely
                continue
        
        if len(covers) == 0:
            raise Exception("Failed to create any covers")
        
        print(f"\n=== Successfully generated {len(covers)} covers ===\n")
        return covers
    
    def generate_single_cover(self, book):
        """
        Generate a single cover based on the book's selected cover style
        """
        from covers.models import Cover
        
        print(f"\n=== Generating Single Cover for Book: {book.title} ===")
        print(f"Cover Style: {book.cover_style.name}")
        
        # Generate AI design concept for the specific style
        try:
            design_concept = self._generate_ai_cover_concept_for_style(book)
            
            if not design_concept:
                raise Exception("Failed to generate design concept for cover style")
            
            print(f"Successfully generated AI design concept: {design_concept.get('concept_name', 'Design')}")
            
        except Exception as e:
            print(f"AI cover generation failed: {str(e)}")
            raise Exception(f"Cover generation failed: {str(e)}")
        
        # Create the cover
        try:
            print(f"\nCreating cover for style: {book.cover_style.name}")
            
            # Generate unique filename
            clean_title = self._clean_filename(book.title)
            filename = f"{clean_title}_cover_final_{random.randint(1000, 9999)}"
            pdf_path = self.covers_dir / f"{filename}.pdf"
            png_path = self.covers_dir / f"{filename}.png"
            
            # Create HTML with AI-generated design
            html_content = self._create_ai_cover_html(book.title, design_concept)
            
            # Render to PDF (assuming we have weasyprint or similar)
            # For now, create a simple ReportLab cover
            self._create_simple_cover_pdf(book.title, design_concept, str(pdf_path))
            
            # Convert PDF to PNG for preview
            self._pdf_to_png(str(pdf_path), str(png_path))
            
            # Create Cover object
            cover = Cover.objects.create(
                book=book,
                template_style=f"ai_{design_concept.get('trend', 'modern')}_guided",
                image_path=f"covers/{png_path.name}",
                pdf_path=f"covers/{pdf_path.name}",
                generation_params={
                    'ai_generated': True,
                    'design_concept': design_concept.get('concept_name', 'Guided Design'),
                    'trend_style': design_concept.get('trend', 'modern'),
                    'colors': design_concept.get('colors', {}),
                    'mood': design_concept.get('mood', 'professional'),
                    'guided_workflow': True,
                }
            )
            # Store metadata and a grid overlay for review
            try:
                self._save_cover_metadata(cover, design_concept)
            finally:
                self._create_grid_overlay(str(png_path))
                self._create_golden_ratio_overlay(str(png_path))
            
            # Automatically select this cover
            cover.select()
            
            print(f"✓ Cover created and selected successfully")
            return cover
            
        except Exception as e:
            print(f"✗ Cover creation failed: {str(e)}")
            raise
    
    def generate_cover_prompts(self, book) -> list:
        """
        Generate 3 ReportLab cover design prompts for a book
        Returns text prompts describing how to render covers using ReportLab
        """
        print(f"\n=== Generating ReportLab Cover Prompts for Book: {book.title} ===")
        
        try:
            # Generate AI cover concepts
            design_concepts = self._generate_ai_cover_concepts(book)
            
            if not design_concepts or len(design_concepts) < 3:
                raise Exception("Failed to generate 3 design concepts from AI")
            
            print(f"Successfully generated {len(design_concepts)} AI design concepts")
            
            # Convert AI concepts to ReportLab prompts
            prompts = []
            for i, concept in enumerate(design_concepts[:3]):
                prompt = self._convert_concept_to_reportlab_prompt(book.title, concept, i+1)
                prompts.append(prompt)
            
            return prompts
            
        except Exception as e:
            print(f"Cover prompt generation failed: {str(e)}")
            # Return fallback prompts
            return self._get_fallback_reportlab_prompts(book.title)
    
    def _convert_concept_to_reportlab_prompt(self, title: str, concept: dict, cover_number: int) -> str:
        """Convert AI design concept to ReportLab rendering prompt"""
        
        trend = concept.get('trend', 'minimalist')
        colors = concept.get('colors', {})
        typography = concept.get('typography', 'Large bold sans-serif title')
        visual_elements = concept.get('visual_elements', 'Simple geometric shapes')
        layout = concept.get('layout', 'Centered title')
        
        # Split title for better layout
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        
        prompt = f"""Cover {cover_number}: {concept.get('concept_name', 'Professional Design')}

Use ReportLab to create a {trend} style cover for the book "{title}".

Canvas Setup:
- Page size: letter (8.5 x 11 inches)
- Background color: {colors.get('background', '#FFFFFF')}

Title Rendering:
- Primary title: "{title_line1}"
{f'- Secondary title: "{title_line2}"' if title_line2 else ''}
- Font: Helvetica-Bold
- Size: 48pt for primary, 32pt for secondary
- Color: {colors.get('primary', '#000000')}
- Position: Centered horizontally, vertically centered
- Line spacing: 1.2

Visual Elements:
- Style: {trend}
- Colors: Primary {colors.get('primary', '#000000')}, Secondary {colors.get('secondary', '#666666')}, Accent {colors.get('accent', '#999999')}
- Elements: {visual_elements}

Layout Instructions:
{layout}

ReportLab Code Structure:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch

def create_cover{cover_number}(c):
    # Set up canvas
    c.setPageSize(letter)
    
    # Background
    c.setFillColor(HexColor('{colors.get('background', '#FFFFFF')}'))
    c.rect(0, 0, 8.5*inch, 11*inch, fill=1)
    
    # Title rendering
    c.setFillColor(HexColor('{colors.get('primary', '#000000')}'))
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(4.25*inch, 6*inch, "{title_line1}")
    {f'c.drawCentredString(4.25*inch, 5.5*inch, "{title_line2}")' if title_line2 else ''}
    
    # Add visual elements based on {trend} style
    # {visual_elements}
```

Accessibility: Ensure high contrast ratio between text and background colors."""
        
        return prompt
    
    def _get_fallback_reportlab_prompts(self, title: str) -> list:
        """Return fallback ReportLab prompts if AI generation fails"""
        
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        cover_a_lines = [
            "Cover A: Modern Minimalist",
            "",
            f'Use ReportLab to create a clean, modern cover for "{title}".',
            "",
            "Canvas Setup:",
            "- Page size: letter (8.5 x 11 inches)",
            "- Background: White (#FFFFFF)",
            "",
            "Title Rendering:",
            f'- Primary title: "{title_line1}"',
        ]
        if title_line2:
            cover_a_lines.append(f'- Secondary title: "{title_line2}"')
        cover_a_lines.extend([
            "- Font: Helvetica-Bold, 48pt primary, 32pt secondary",
            "- Color: Navy blue (#1a365d)",
            "- Position: Centered",
            "",
            "Visual Elements:",
            "- Add a simple colored rectangle background",
            "- Use HexColor('#e2e8f0') for background shape",
            "",
            "ReportLab Code:",
            "```python",
            "from reportlab.lib.pagesizes import letter",
            "from reportlab.pdfgen import canvas",
            "from reportlab.lib.colors import HexColor",
            "",
            "def create_coverA(c):",
            "    c.setPageSize(letter)",
            "    c.setFillColor(HexColor('#e2e8f0'))",
            "    c.rect(0.5*inch, 0.5*inch, 7.5*inch, 10*inch, fill=1)",
            "    c.setFillColor(HexColor('#1a365d'))",
            '    c.setFont("Helvetica-Bold", 48)',
            f'    c.drawCentredString(4.25*inch, 6*inch, "{title_line1}")',
        ])
        if title_line2:
            cover_a_lines.append(f'    c.drawCentredString(4.25*inch, 5.5*inch, "{title_line2}")')
        cover_a_lines.append("```")

        cover_b_lines = [
            "Cover B: Elegant Typography",
            "",
            f'Use ReportLab to create an elegant typographic cover for "{title}".',
            "",
            "Canvas Setup:",
            "- Page size: letter",
            "- Background: Light gray gradient (#f8fafc to #e2e8f0)",
            "",
            "Title Rendering:",
            f'- Primary title: "{title_line1}"',
        ]
        if title_line2:
            cover_b_lines.append(f'- Secondary title: "{title_line2}"')
        cover_b_lines.extend([
            "- Font: Helvetica-Bold, 52pt primary, 36pt secondary",
            "- Color: Dark blue (#2d3748)",
            "- Position: Left-aligned with margin",
            "",
            "Visual Elements:",
            "- Add decorative line under title",
            "- Use subtle background pattern",
            "",
            "ReportLab Code:",
            "```python",
            "from reportlab.lib.pagesizes import letter",
            "from reportlab.pdfgen import canvas",
            "from reportlab.lib.colors import HexColor",
            "",
            "def create_coverB(c):",
            "    c.setPageSize(letter)",
            "    # Gradient background simulation",
            "    c.setFillColor(HexColor('#f8fafc'))",
            "    c.rect(0, 0, 8.5*inch, 11*inch, fill=1)",
            "    c.setFillColor(HexColor('#2d3748'))",
            '    c.setFont("Helvetica-Bold", 52)',
            f'    c.drawString(1*inch, 7*inch, "{title_line1}")',
        ])
        if title_line2:
            cover_b_lines.extend([
                '    c.setFont("Helvetica-Bold", 36)',
                f'    c.drawString(1*inch, 6.5*inch, "{title_line2}")',
            ])
        cover_b_lines.extend([
            "    # Decorative line",
            "    c.setStrokeColor(HexColor('#4a5568'))",
            "    c.setLineWidth(3)",
            "    c.line(1*inch, 6*inch, 7.5*inch, 6*inch)",
            "```",
        ])

        cover_c_lines = [
            "Cover C: Bold Statement",
            "",
            f'Use ReportLab to create a bold, striking cover for "{title}".',
            "",
            "Canvas Setup:",
            "- Page size: letter",
            "- Background: Dark with light text (#1a202c)",
            "",
            "Title Rendering:",
            f'- Primary title: "{title_line1}"',
        ]
        if title_line2:
            cover_c_lines.append(f'- Secondary title: "{title_line2}"')
        cover_c_lines.extend([
            "- Font: Helvetica-Bold, 56pt primary, 40pt secondary",
            "- Color: White (#ffffff)",
            "- Position: Centered",
            "",
            "Visual Elements:",
            "- High contrast design",
            "- Bold background shapes",
            "",
            "ReportLab Code:",
            "```python",
            "from reportlab.lib.pagesizes import letter",
            "from reportlab.pdfgen import canvas",
            "from reportlab.lib.colors import HexColor",
            "",
            "def create_coverC(c):",
            "    c.setPageSize(letter)",
            "    c.setFillColor(HexColor('#1a202c'))",
            "    c.rect(0, 0, 8.5*inch, 11*inch, fill=1)",
            "    c.setFillColor(HexColor('#ffffff'))",
            '    c.setFont("Helvetica-Bold", 56)',
            f'    c.drawCentredString(4.25*inch, 6*inch, "{title_line1}")',
        ])
        if title_line2:
            cover_c_lines.extend([
                '    c.setFont("Helvetica-Bold", 40)',
                f'    c.drawCentredString(4.25*inch, 5.5*inch, "{title_line2}")',
            ])
        cover_c_lines.append("```")

        return [
            "\n".join(cover_a_lines),
            "\n".join(cover_b_lines),
            "\n".join(cover_c_lines),
        ]
        """
        Generate 3 AI-powered cover designs for a book
        NO FALLBACK TEMPLATES - All designs are AI-generated
        """
        from covers.models import Cover
        
        print(f"\n=== Generating AI Covers for Book: {book.title} ===")
        print(f"Sub-niche: {book.niche.name}")
        print(f"Audience: {self._infer_audience(book.niche.name)}")
        
        covers = []
        
        # Generate AI ReportLab design concepts
        try:
            design_concepts = self._generate_ai_reportlab_concepts(book)
            
            if not design_concepts or len(design_concepts) < 3:
                raise Exception("Failed to generate 3 design concepts from AI")
            
            print(f"Successfully generated {len(design_concepts)} AI design concepts")
            
        except Exception as e:
            print(f"AI cover generation failed: {str(e)}")
            raise Exception(f"Cover generation failed: {str(e)}")
        
        # Create covers from AI concepts
        for i, concept in enumerate(design_concepts[:3]):  # Ensure exactly 3
            try:
                print(f"\nCreating cover {i+1}/3: {concept.get('concept_name', 'Design')}")
                
                # Generate unique filename
                clean_title = self._clean_filename(book.title)
                filename = f"{clean_title}_cover_{i+1}_{random.randint(1000, 9999)}"
                image_path = self.covers_dir / f"{filename}.png"
                pdf_path = self.covers_dir / f"{filename}.pdf"
                
                # Create HTML with AI-generated design
                html_content = self._create_ai_cover_html(book.title, concept)
                
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
                    template_style=f"ai_{concept.get('trend', 'modern')}_{i+1}",
                    image_path=f"covers/{image_path.name}",
                    pdf_path=f"covers/{pdf_path.name}",
                    generation_params={
                        'ai_generated': True,
                        'design_concept': concept.get('concept_name', 'Professional Design'),
                        'trend_style': concept.get('trend', 'modern'),
                        'colors': concept.get('colors', {}),
                        'mood': concept.get('mood', 'professional'),
                    }
                )
                covers.append(cover)
                print(f"✓ Cover {i+1} created successfully")
                
            except Exception as e:
                print(f"✗ Cover {i+1} creation failed: {str(e)}")
                # Continue to try next cover instead of failing completely
                continue
        
        if len(covers) == 0:
            raise Exception("Failed to create any covers")
        
        print(f"\n=== Successfully generated {len(covers)} covers ===\n")
        return covers
    
    def generate_single_cover(self, book):
        """
        Generate a single cover based on the book's selected cover style
        """
        from covers.models import Cover
        
        print(f"\n=== Generating Single Cover for Book: {book.title} ===")
        print(f"Cover Style: {book.cover_style.name}")
        
        # Generate AI design concept for the specific style
        try:
            design_concept = self._generate_ai_cover_concept_for_style(book)
            
            if not design_concept:
                raise Exception("Failed to generate design concept for cover style")
            
            print(f"Successfully generated AI design concept: {design_concept.get('concept_name', 'Design')}")
            
        except Exception as e:
            print(f"AI cover generation failed: {str(e)}")
            raise Exception(f"Cover generation failed: {str(e)}")
        
        # Create the cover
        try:
            print(f"\nCreating cover for style: {book.cover_style.name}")
            
            # Generate unique filename
            clean_title = self._clean_filename(book.title)
            filename = f"{clean_title}_cover_final_{random.randint(1000, 9999)}"
            pdf_path = self.covers_dir / f"{filename}.pdf"
            png_path = self.covers_dir / f"{filename}.png"
            
            # Create HTML with AI-generated design
            html_content = self._create_ai_cover_html(book.title, design_concept)
            
            # Render to PDF (assuming we have weasyprint or similar)
            # For now, create a simple ReportLab cover
            self._create_simple_cover_pdf(book.title, design_concept, str(pdf_path))
            
            # Convert PDF to PNG for preview
            self._pdf_to_png(str(pdf_path), str(png_path))
            
            # Create Cover object
            cover = Cover.objects.create(
                book=book,
                template_style=f"ai_{design_concept.get('trend', 'modern')}_guided",
                image_path=f"covers/{png_path.name}",
                pdf_path=f"covers/{pdf_path.name}",
                generation_params={
                    'ai_generated': True,
                    'design_concept': design_concept.get('concept_name', 'Guided Design'),
                    'trend_style': design_concept.get('trend', 'modern'),
                    'colors': design_concept.get('colors', {}),
                    'mood': design_concept.get('mood', 'professional'),
                    'guided_workflow': True,
                }
            )
            
            # Automatically select this cover
            cover.select()
            
            print(f"✓ Cover created and selected successfully")
            return cover
            
        except Exception as e:
            print(f"✗ Cover creation failed: {str(e)}")
            raise
    
    def _generate_ai_reportlab_concepts(self, book) -> list:
        """Generate AI-powered ReportLab design concepts"""
        
        # Get trending context for the niche
        trending_ctx = get_trending_context(book.niche.name)
        trending_summary = f"{trending_ctx.get('category', 'Professional')} - {', '.join(trending_ctx.get('trends_2025', [])[:3])}"
        
        prompt = REPORTLAB_COVER_PROMPT.format(
            title=book.title,
            audience=self._infer_audience(book.niche.name),
            sub_niche=book.niche.name,
            trending_info=trending_summary
        )
        
        try:
            # Use Cloudflare AI instead of OpenRouter
            if self.cloudflare_client:
                print("🌩️  Using Cloudflare AI for cover design generation")
                system_prompt = "You are a creative ReportLab graphics designer who creates professional PDF book covers. Always respond with ONLY valid JSON, no markdown code blocks or extra text."
                full_prompt = f"{system_prompt}\n\n{prompt}"
                
                result = self.cloudflare_client.call_model(
                    prompt=full_prompt,
                    max_tokens=4000,
                    temperature=0.8
                )
                
                if not result.get('success'):
                    print(f"⚠️  Cloudflare AI failed: {result.get('error')}, using fallback")
                    raise Exception(f"Cloudflare API failed: {result.get('error')}")
                
                content = result.get('response', '')
                print(f"✓ Cloudflare AI response received ({len(content)} chars)")
            else:
                # No Cloudflare available, use fallback
                print("⚠️  No AI available, using fallback designs")
                raise Exception("No AI client available for cover generation")
            
            # Clean up response (remove markdown code blocks if present)
            content_clean = content.strip()
            if content_clean.startswith('```'):
                # Remove code block markers
                lines = content_clean.split('\n')
                content_clean = '\n'.join(lines[1:-1]) if len(lines) > 2 else content_clean
                content_clean = content_clean.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON response
            try:
                result = json.loads(content_clean)
                designs = result.get('designs', [])
                
                if isinstance(designs, list) and len(designs) >= 3:
                    print(f"Successfully parsed {len(designs)} ReportLab cover designs from AI")
                    return designs[:3]
                else:
                    print(f"AI returned insufficient designs: {len(designs) if isinstance(designs, list) else 0}")
                    raise ValueError("AI did not return 3 ReportLab cover designs")
            
            except json.JSONDecodeError as je:
                print(f"Failed to parse JSON response: {je}")
                print(f"Raw response (first 500 chars): {content[:500]}")
                raise Exception("AI returned invalid JSON for ReportLab cover designs")
        
        except Exception as e:
            print(f"❌ Cover concept generation error: {str(e)}")
            print("⚠️  Falling back to default designs")
            # Return fallback designs instead of failing
            return self._get_fallback_designs()
    
    def _create_reportlab_cover_pdf(self, book, concept: dict, pdf_path: str):
        """Create a ReportLab PDF cover using AI-generated code"""
        
        try:
            # Get the ReportLab code from the concept
            reportlab_code = concept.get('reportlab_code', '')
            
            if not reportlab_code:
                raise Exception("No ReportLab code provided in concept")
            
            # Create a canvas
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            # Execute the AI-generated ReportLab code
            # Note: In a production environment, you'd want to sandbox this execution
            # For now, we'll create a safe execution environment
            
            # Set up the execution context with safe imports
            exec_globals = {
                'canvas': c,
                'letter': letter,
                'inch': inch,
                'cm': cm,
                'HexColor': HexColor,
                'colors': colors,
                'Drawing': Drawing,
                'Rect': Rect,
                'String': String,
                'Line': Line,
                'Circle': Circle,
                'Polygon': Polygon,
                'renderPDF': renderPDF,
                'TA_CENTER': TA_CENTER,
                'TA_JUSTIFY': TA_JUSTIFY,
                'TA_LEFT': TA_LEFT,
                'TA_RIGHT': TA_RIGHT,
            }
            
            # Extract function definitions from the code
            lines = reportlab_code.split('\n')
            functions = []
            current_function = []
            in_function = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('def create_cover') and '(' in line:
                    if current_function:
                        functions.append('\n'.join(current_function))
                    current_function = [line]
                    in_function = True
                elif in_function:
                    current_function.append(line)
                    if line.startswith('def ') and '(' in line:
                        # New function starts
                        functions.append('\n'.join(current_function[:-1]))
                        current_function = [line]
                    elif not line or line.startswith('#'):
                        continue
            
            if current_function:
                functions.append('\n'.join(current_function))
            
            # Execute the functions and find the appropriate one to call
            cover_function = None
            for func_code in functions:
                if 'def create_cover' in func_code:
                    try:
                        exec(func_code, exec_globals)
                        # Find the function name
                        for line in func_code.split('\n'):
                            if line.strip().startswith('def '):
                                func_name = line.split('(')[0].replace('def ', '').strip()
                                if func_name.startswith('create_cover'):
                                    cover_function = func_name
                                    break
                        if cover_function:
                            break
                    except Exception as e:
                        print(f"Failed to execute function: {e}")
                        continue
            
            # Call the cover creation function
            if cover_function and cover_function in exec_globals:
                try:
                    exec_globals[cover_function](c)
                    c.save()
                    print(f"✓ ReportLab cover PDF created: {pdf_path}")
                except Exception as e:
                    print(f"Failed to call cover function {cover_function}: {e}")
                    raise Exception(f"ReportLab execution failed: {str(e)}")
            else:
                raise Exception("No valid cover creation function found")
            
        except Exception as e:
            print(f"ReportLab PDF creation error: {str(e)}")
            # Create a fallback simple cover
            self._create_fallback_reportlab_cover(book, concept, pdf_path)
    
    def _smart_wrap_title(self, canvas_obj, text: str, max_width: float, font_name: str, initial_font_size: int) -> list:
        """
        Smart text wrapping that considers actual text width in ReportLab
        
        Args:
            canvas_obj: ReportLab canvas object
            text: Title text to wrap
            max_width: Maximum width in points/inches
            font_name: Font name to use
            initial_font_size: Starting font size
        
        Returns:
            List of text lines that fit within max_width
        """
        canvas_obj.setFont(font_name, initial_font_size)
        
        # Check if the whole title fits on one line
        text_width = canvas_obj.stringWidth(text, font_name, initial_font_size)
        if text_width <= max_width:
            return [text]
        
        # Split by natural break points: colons, semicolons, em-dashes
        if ':' in text:
            parts = text.split(':', 1)
            line1 = parts[0].strip()
            line2 = parts[1].strip()
            
            # Check if both parts fit on their own lines
            width1 = canvas_obj.stringWidth(line1, font_name, initial_font_size)
            width2 = canvas_obj.stringWidth(line2, font_name, initial_font_size * 0.9)
            
            if width1 <= max_width and width2 <= max_width:
                return [line1, line2]
        
        # Fall back to word-based wrapping
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = canvas_obj.stringWidth(test_line, font_name, initial_font_size)
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limit to 3 lines maximum for aesthetics
        if len(lines) > 3:
            # Combine into 3 lines by redistributing words
            total_words = text.split()
            third = len(total_words) // 3
            lines = [
                ' '.join(total_words[:third]),
                ' '.join(total_words[third:third*2]),
                ' '.join(total_words[third*2:])
            ]
        
        return lines if lines else [text]
    
    def _create_fallback_reportlab_cover(self, book=None, concept: dict = None, pdf_path: str = ""):
        """Create a deterministic premium cover when AI rendering fails."""

        concept = concept or {}
        title = getattr(book, 'title', concept.get('title', 'Professional Guide'))

        try:
            canvas_obj = canvas.Canvas(pdf_path, pagesize=letter)
            template = resolve_template(concept.get('trend'))

            domain_slug = ""
            subtitle = template.subtitle_text
            if book and getattr(book, 'domain', None):
                domain_slug = getattr(book.domain, 'slug', '') or ""
                subtitle = getattr(book.domain, 'name', subtitle)

            palette_override = concept.get('colors') or None

            engine = CoverLayoutEngine(
                canvas_obj,
                template,
                palette_override=palette_override,
                subtitle_override=subtitle,
                domain_slug=domain_slug,
            )
            engine.render_cover(title)
            canvas_obj.save()
            print(f"✓ Fallback premium cover created: {pdf_path}")

        except Exception as err:
            print(f"Fallback layout engine error: {err}")
            self._create_legacy_fallback_cover(title, pdf_path)

    def _create_legacy_fallback_cover(self, title: str, pdf_path: str):
        """Legacy simple cover generator retained as a last resort."""

        try:
            c = canvas.Canvas(pdf_path, pagesize=letter)

            c.setFillColor(HexColor('#f8fafc'))
            c.rect(0, 0, 8.5 * inch, 11 * inch, fill=1)

            c.setFillColor(HexColor('#1a365d'))
            title_lines = self._smart_wrap_title(c, title, max_width=7 * inch, font_name="Helvetica-Bold", initial_font_size=48)

            if len(title_lines) == 1:
                font_size = 48 if len(title_lines[0]) < 40 else 42
            elif len(title_lines) == 2:
                font_size = 40 if max(len(line) for line in title_lines) < 30 else 36
            else:
                font_size = 32

            line_height = font_size * 1.2
            start_y = 6.5 * inch if len(title_lines) <= 2 else 6.8 * inch

            for index, line in enumerate(title_lines):
                weight = font_size if index == 0 else font_size * 0.9
                c.setFont("Helvetica-Bold", weight)
                y_position = start_y - (index * line_height * 0.8)
                c.drawCentredString(4.25 * inch, y_position, line)

            c.setFillColor(HexColor('#4a5568'))
            c.setFont("Helvetica", 24)
            c.drawCentredString(4.25 * inch, 4.5 * inch, "Professional Guide")

            c.save()
            print(f"✓ Legacy fallback cover created: {pdf_path}")

        except Exception as e:
            print(f"Legacy fallback cover creation failed: {e}")
            raise
    
    def _get_fallback_designs(self) -> list:
        """Return simple fallback designs when AI is not available"""
        return [
            {
                'trend': 'minimalist_modern',
                'concept_name': 'Clean Professional',
                'reportlab_code': '',
                'colors': {
                    'primary': '#1a365d',
                    'secondary': '#4a5568',
                    'accent': '#3b82f6',
                    'background': '#ffffff'
                },
                'layout_description': 'Centered title with clean background',
                'accessibility_notes': 'High contrast'
            },
            {
                'trend': 'elegant_serif',
                'concept_name': 'Professional Elegant',
                'reportlab_code': '',
                'colors': {
                    'primary': '#2d3748',
                    'secondary': '#718096',
                    'accent': '#4299e1',
                    'background': '#f7fafc'
                },
                'layout_description': 'Elegant serif typography',
                'accessibility_notes': 'AAA compliant'
            },
            {
                'trend': 'modern_bold',
                'concept_name': 'Bold Impact',
                'reportlab_code': '',
                'colors': {
                    'primary': '#000000',
                    'secondary': '#4a5568',
                    'accent': '#dc2626',
                    'background': '#ffffff'
                },
                'layout_description': 'Bold statement design',
                'accessibility_notes': 'Maximum contrast'
            }
        ]
    
    def _infer_audience(self, sub_niche: str) -> str:
        """Infer audience from sub-niche"""
        kids_signals = ['kids', 'preschool', 'family', 'children', 'parenting']
        niche_lower = sub_niche.lower()
        
        if any(sig in niche_lower for sig in kids_signals):
            return "Parents, caregivers, and early educators"
        
        return "Modern professionals and lifelong learners"
    
    def _clean_filename(self, title: str) -> str:
        """Clean title for filename"""
        cleaned = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
        cleaned = cleaned[:80]
        cleaned = '_'.join(cleaned.split())
        return cleaned or "Professional_Book"
    
    def _create_ai_cover_html(self, title: str, concept: dict) -> str:
        """Create HTML for AI-generated cover design"""
        
        trend = concept.get('trend', 'modern')
        colors = self._ensure_contrast(concept.get('colors', {}))
        
        # Split title for better layout
        words = title.split()
        if len(words) > 4:
            mid = len(words) // 2
            title_line1 = ' '.join(words[:mid])
            title_line2 = ' '.join(words[mid:])
        else:
            title_line1 = title
            title_line2 = ""
        
        # Route to appropriate template based on trend
        if 'glass' in trend.lower():
            return self._glassmorphism_template(title_line1, title_line2, colors, concept)
        elif 'neo' in trend.lower():
            return self._neomorphism_template(title_line1, title_line2, colors, concept)
        elif 'brutal' in trend.lower():
            return self._brutalist_template(title_line1, title_line2, colors, concept)
        elif 'organic' in trend.lower():
            return self._organic_template(title_line1, title_line2, colors, concept)
        elif 'cyber' in trend.lower() or 'futur' in trend.lower():
            return self._cyberpunk_template(title_line1, title_line2, colors, concept)
        elif 'vintage' in trend.lower():
            return self._vintage_modern_template(title_line1, title_line2, colors, concept)
        else:  # minimalist or default
            return self._minimalist_template(title_line1, title_line2, colors, concept)
    
    def _glassmorphism_template(self, title1: str, title2: str, colors: dict, concept: dict) -> str:
        """Glassmorphism design template"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700;900&family=Poppins:wght@300;600;800&display=swap');
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, {colors.get('background', '#f8fafc')} 0%, {colors.get('primary', '#e2e8f0')}40 100%);
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
                    padding: 100px 80px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
                    position: relative;
                    z-index: 10;
                    max-width: 1200px;
                    text-align: center;
                }}
                
                .bg-shape {{
                    position: absolute;
                    width: 700px;
                    height: 700px;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 50%;
                    top: -200px;
                    right: -200px;
                    backdrop-filter: blur(40px);
                }}
                
                .title {{
                    font-family: 'Poppins', sans-serif;
                    font-size: 120px;
                    font-weight: 800;
                    line-height: 1.1;
                    margin-bottom: 30px;
                    color: {colors.get('primary', '#1a365d')};
                    text-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    letter-spacing: -3px;
                }}
                
                .title-line-2 {{
                    font-size: 80px;
                    font-weight: 700;
                    margin-top: 20px;
                }}
                
                .subtitle {{
                    font-size: 32px;
                    font-weight: 300;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    color: {colors.get('secondary', '#4a5568')};
                    opacity: 0.9;
                    margin-top: 50px;
                }}
                
                .accent-element {{
                    width: 180px;
                    height: 6px;
                    background: linear-gradient(90deg, {colors.get('accent', '#3b82f6')}, transparent);
                    margin: 50px auto 0;
                    border-radius: 3px;
                }}
            </style>
        </head>
        <body>
            <div class="bg-shape"></div>
            <div class="glass-card">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Professional Guide</div>
                <div class="accent-element"></div>
            </div>
        </body>
        </html>
        """
    
    def _neomorphism_template(self, title1: str, title2: str, colors: dict, concept: dict) -> str:
        """Neomorphism soft shadow design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;600;800&display=swap');
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: {colors.get('background', '#f1f5f9')};
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    font-family: 'Nunito', sans-serif;
                }}
                
                .neo-card {{
                    background: {colors.get('background', '#f1f5f9')};
                    border-radius: 40px;
                    padding: 120px 100px;
                    box-shadow: 
                        25px 25px 50px rgba(0,0,0,0.12),
                        -25px -25px 50px rgba(255,255,255,0.9);
                    position: relative;
                    max-width: 1200px;
                    text-align: center;
                }}
                
                .title {{
                    font-size: 110px;
                    font-weight: 800;
                    line-height: 1.1;
                    margin-bottom: 30px;
                    color: {colors.get('primary', '#2d3748')};
                    letter-spacing: -2px;
                }}
                
                .title-line-2 {{
                    font-size: 75px;
                    font-weight: 700;
                    margin-top: 20px;
                }}
                
                .subtitle {{
                    font-size: 30px;
                    font-weight: 300;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    color: {colors.get('secondary', '#4a5568')};
                    margin-top: 40px;
                }}
            </style>
        </head>
        <body>
            <div class="neo-card">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Master Guide</div>
            </div>
        </body>
        </html>
        """
    
    def _brutalist_template(self, title1: str, title2: str, colors: dict, concept: dict) -> str:
        """Bold brutalist design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@700&display=swap');
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: {colors.get('primary', '#000000')};
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    font-family: 'Oswald', sans-serif;
                    position: relative;
                }}
                
                .content {{
                    background: {colors.get('background', '#ffffff')};
                    padding: 100px;
                    position: relative;
                    z-index: 10;
                    max-width: 1200px;
                    text-align: center;
                    box-shadow: 25px 25px 0px {colors.get('accent', '#dc2626')};
                    border: 10px solid {colors.get('primary', '#000000')};
                }}
                
                .title {{
                    font-family: 'Bebas Neue', sans-serif;
                    font-size: 160px;
                    line-height: 0.9;
                    margin-bottom: 30px;
                    color: {colors.get('primary', '#000000')};
                    text-transform: uppercase;
                    letter-spacing: 6px;
                }}
                
                .title-line-2 {{
                    font-size: 120px;
                    margin-top: 15px;
                }}
                
                .subtitle {{
                    font-size: 48px;
                    font-weight: 700;
                    letter-spacing: 12px;
                    text-transform: uppercase;
                    color: {colors.get('accent', '#dc2626')};
                    margin-top: 40px;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">GUIDE</div>
            </div>
        </body>
        </html>
        """
    
    def _organic_template(self, title1: str, title2: str, colors: dict, concept: dict) -> str:
        """Organic flowing shapes design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Lato:wght@300&display=swap');
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, {colors.get('background', '#f0fdf4')} 0%, {colors.get('primary', '#10b981')}60 100%);
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
                    width: 800px;
                    height: 800px;
                    background: rgba(255, 255, 255, 0.25);
                    border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
                    top: -200px;
                    right: -200px;
                    backdrop-filter: blur(25px);
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
                    letter-spacing: -3px;
                }}
                
                .title-line-2 {{
                    font-size: 90px;
                    font-weight: 700;
                    margin-top: 25px;
                }}
                
                .subtitle {{
                    font-size: 36px;
                    font-weight: 300;
                    letter-spacing: 12px;
                    text-transform: uppercase;
                    color: {colors.get('accent', '#059669')};
                    margin-top: 50px;
                }}
            </style>
        </head>
        <body>
            <div class="organic-shape"></div>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Natural Guide</div>
            </div>
        </body>
        </html>
        """
    
    def _cyberpunk_template(self, title1: str, title2: str, colors: dict, concept: dict) -> str:
        """Futuristic cyberpunk neon design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;800&display=swap');
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
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
                        linear-gradient(rgba(139, 92, 246, 0.15) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(139, 92, 246, 0.15) 1px, transparent 1px);
                    background-size: 60px 60px;
                }}
                
                .neon-glow {{
                    position: absolute;
                    width: 700px;
                    height: 700px;
                    background: radial-gradient(circle, {colors.get('accent', '#ec4899')}50 0%, transparent 70%);
                    top: -150px;
                    right: -150px;
                    filter: blur(60px);
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
                        0 0 25px {colors.get('accent', '#ec4899')},
                        0 0 50px {colors.get('accent', '#ec4899')};
                    letter-spacing: -2px;
                    text-transform: uppercase;
                }}
                
                .title-line-2 {{
                    font-size: 100px;
                    font-weight: 700;
                    margin-top: 25px;
                }}
                
                .subtitle {{
                    font-size: 38px;
                    font-weight: 600;
                    letter-spacing: 10px;
                    text-transform: uppercase;
                    color: {colors.get('secondary', '#8b5cf6')};
                    margin-top: 50px;
                    text-shadow: 0 0 15px {colors.get('secondary', '#8b5cf6')};
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
            </div>
        </body>
        </html>
        """
    
    def _vintage_modern_template(self, title1: str, title2: str, colors: dict, concept: dict) -> str:
        """Vintage modern design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@600;700&family=Poppins:wght@300;600&display=swap');
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                body {{
                    width: 1600px;
                    height: 2400px;
                    background: linear-gradient(135deg, {colors.get('background', '#fef3c7')} 0%, {colors.get('primary', '#f59e0b')}40 100%);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 150px;
                    font-family: 'Poppins', sans-serif;
                    position: relative;
                }}
                
                .content {{
                    background: rgba(255, 255, 255, 0.95);
                    padding: 100px;
                    border-radius: 20px;
                    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
                    position: relative;
                    z-index: 10;
                    max-width: 1100px;
                    text-align: center;
                    border: 8px solid {colors.get('secondary', '#d97706')};
                }}
                
                .title {{
                    font-family: 'Crimson Text', serif;
                    font-size: 120px;
                    font-weight: 700;
                    line-height: 1.1;
                    margin-bottom: 40px;
                    color: {colors.get('secondary', '#92400e')};
                    letter-spacing: -1px;
                }}
                
                .title-line-2 {{
                    font-size: 85px;
                    font-weight: 600;
                    margin-top: 25px;
                }}
                
                .subtitle {{
                    font-size: 34px;
                    font-weight: 300;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    color: {colors.get('accent', '#f59e0b')};
                    margin-top: 50px;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                <div class="title">{title1}</div>
                {f'<div class="title title-line-2">{title2}</div>' if title2 else ''}
                <div class="subtitle">Timeless Guide</div>
            </div>
        </body>
        </html>
        """
    
    def _minimalist_template(self, title1: str, title2: str, colors: dict, concept: dict) -> str:
        """Clean minimalist design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600;900&display=swap');
                
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
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
                
                .geometric-bg {{
                    position: absolute;
                    width: 900px;
                    height: 900px;
                    background: linear-gradient(45deg, {colors.get('primary', '#3b82f6')}15, {colors.get('accent', '#60a5fa')}15);
                    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
                    top: -250px;
                    right: -250px;
                    opacity: 0.15;
                }}
                
                .content {{
                    position: relative;
                    z-index: 10;
                    text-align: center;
                    max-width: 1200px;
                }}
                
                .title {{
                    font-size: 140px;
                    font-weight: 900;
                    line-height: 1.1;
                    margin-bottom: 50px;
                    color: {colors.get('primary', '#1a365d')};
                    letter-spacing: -4px;
                }}
                
                .title-line-2 {{
                    font-size: 100px;
                    font-weight: 700;
                    margin-top: 25px;
                }}
                
                .subtitle {{
                    font-size: 38px;
                    font-weight: 300;
                    letter-spacing: 14px;
                    text-transform: uppercase;
                    color: {colors.get('secondary', '#4a5568')};
                    margin-top: 50px;
                }}
                
                .minimal-line {{
                    width: 350px;
                    height: 4px;
                    background: {colors.get('accent', '#3b82f6')};
                    margin: 50px auto 0;
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
    
    def _pdf_to_png(self, pdf_path: str, png_path: str):
        """Convert PDF to PNG for preview"""
        try:
            # Try pdf2image first
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
                if images:
                    images[0].save(png_path, 'PNG')
                    print(f"✓ PNG preview created: {png_path}")
                    return
            except (ImportError, Exception) as e:
                # Common case: poppler not installed on Linux for pdf2image
                msg = str(e)
                if 'poppler' in msg.lower() or 'PDFInfoNotInstalledError' in msg:
                    print("pdf2image failed: Poppler not found. On Linux, install it with: sudo apt-get install -y poppler-utils")
                else:
                    print(f"pdf2image not available or failed: {e}")
                print("→ Falling back to PyMuPDF renderer (no system deps)...")
            
            # Try PyMuPDF
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(pdf_path)
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                pix.save(png_path)
                print(f"✓ PNG preview created with PyMuPDF: {png_path}")
                return
            except (ImportError, Exception) as e:
                print(f"PyMuPDF not available or failed: {e}, using placeholder fallback...")
            
        except Exception as e:
            print(f"PNG conversion error: {e}")
        
        # Fallback: Create placeholder image
        try:
            img = PILImage.new('RGB', (600, 900), color='white')
            draw = ImageDraw.Draw(img)
            draw.rectangle([50, 50, 550, 850], outline="gray", width=5)
            draw.text((300, 450), "Cover Preview", fill='gray', anchor="mm")
            img.save(png_path, 'PNG')
            print(f"✓ Fallback PNG created: {png_path}")
        except Exception as e:
            print(f"Fallback PNG creation error: {e}")
    
    def generate_single_cover(self, book):
        """
        Generate a single cover based on the book's selected cover style
        """
        from covers.models import Cover
        
        print(f"\n=== Generating Single Cover for Book: {book.title} ===")
        print(f"Cover Style: {book.cover_style.name}")
        
        # Generate AI design concept for the specific style
        try:
            design_concept = self._generate_ai_cover_concept_for_style(book)
            
            if not design_concept:
                raise Exception("Failed to generate design concept for cover style")
            
            print(f"Successfully generated AI design concept: {design_concept.get('concept_name', 'Design')}")
            
        except Exception as e:
            print(f"AI cover generation failed: {str(e)}")
            raise Exception(f"Cover generation failed: {str(e)}")
        
        # Create the cover
        try:
            print(f"\nCreating cover for style: {book.cover_style.name}")
            
            # Generate unique filename
            clean_title = self._clean_filename(book.title)
            filename = f"{clean_title}_cover_final_{random.randint(1000, 9999)}"
            pdf_path = self.covers_dir / f"{filename}.pdf"
            png_path = self.covers_dir / f"{filename}.png"
            
            # Create simple ReportLab cover
            self._create_simple_cover_pdf(book.title, design_concept, str(pdf_path))
            
            # Convert PDF to PNG for preview
            self._pdf_to_png(str(pdf_path), str(png_path))
            
            # Create Cover object
            cover = Cover.objects.create(
                book=book,
                template_style=f"ai_{design_concept.get('trend', 'modern')}_guided",
                image_path=f"covers/{png_path.name}",
                pdf_path=f"covers/{pdf_path.name}",
                generation_params={
                    'ai_generated': True,
                    'design_concept': design_concept.get('concept_name', 'Guided Design'),
                    'trend_style': design_concept.get('trend', 'modern'),
                    'colors': design_concept.get('colors', {}),
                    'mood': design_concept.get('mood', 'professional'),
                    'guided_workflow': True,
                }
            )
            
            # Automatically select this cover
            cover.select()
            
            print(f"✓ Cover created and selected successfully")
            return cover
            
        except Exception as e:
            print(f"✗ Cover creation failed: {str(e)}")
            raise
    
    def _get_style_color_schemes(self, cover_style: str) -> dict:
        """
        Return predefined color schemes for each cover style to ensure visual distinction
        """
        color_schemes = {
            'minimalist': {
                'primary': '#1a365d',  # Deep Navy
                'secondary': '#4a5568',  # Gray
                'accent': '#3b82f6',  # Blue
                'background': '#ffffff'  # White
            },
            'futuristic': {
                'primary': '#ec4899',  # Hot Pink
                'secondary': '#8b5cf6',  # Purple
                'accent': '#06b6d4',  # Cyan
                'background': '#000000'  # Black
            },
            'playful': {
                'primary': '#f59e0b',  # Amber
                'secondary': '#10b981',  # Emerald
                'accent': '#f97316',  # Orange
                'background': '#fef3c7'  # Light Yellow
            },
            'elegant': {
                'primary': '#92400e',  # Brown
                'secondary': '#d97706',  # Gold
                'accent': '#fbbf24',  # Yellow Gold
                'background': '#fefce8'  # Cream
            },
            'corporate': {
                'primary': '#1e293b',  # Dark Slate
                'secondary': '#475569',  # Slate
                'accent': '#0ea5e9',  # Sky Blue
                'background': '#f8fafc'  # Light Gray
            },
            'artistic': {
                'primary': '#7c2d12',  # Deep Red-Brown
                'secondary': '#dc2626',  # Red
                'accent': '#fbbf24',  # Gold
                'background': '#fef2f2'  # Light Pink
            }
        }
        
        return color_schemes.get(cover_style, color_schemes['minimalist'])
    
    def _generate_ai_cover_concept_for_style(self, book) -> dict:
        """Generate AI design concept specifically for the selected cover style"""
        
        # Get trending context for the niche
        trending_ctx = get_trending_context(book.niche.name)
        trending_summary = f"{trending_ctx.get('category', 'Professional')} - {', '.join(trending_ctx.get('trends_2025', [])[:3])}"
        
        # Map cover style to trend
        style_to_trend = {
            'minimalist': 'minimalist_abstract',
            'futuristic': 'cyberpunk_futuristic', 
            'playful': 'organic_shapes',
            'elegant': 'vintage_modern',
            'corporate': 'professional_minimal',
            'artistic': 'abstract_art'
        }
        
        target_trend = style_to_trend.get(book.cover_style.style, 'minimalist_abstract')
        
        # Get predefined colors for this style
        predefined_colors = self._get_style_color_schemes(book.cover_style.style)
        
        prompt = f"""
You are a senior book cover art director specializing in {target_trend} design aesthetics. Generate a single, professional cover design specifically for the {book.cover_style.name} style.

Book Details:
Title: "{book.title}"
Audience: {self._infer_audience(book.niche.name)}
Niche: "{book.niche.name}"
Cover Style: {book.cover_style.name} - {book.cover_style.description}
Trending Context: {trending_summary}

IMPORTANT - Use these EXACT predefined colors for visual distinction:
Primary: {predefined_colors['primary']}
Secondary: {predefined_colors['secondary']}
Accent: {predefined_colors['accent']}
Background: {predefined_colors['background']}

Requirements:
- Design must perfectly match the {book.cover_style.name} style
- Use the ACTUAL BOOK TITLE "{book.title}" prominently
- Use the EXACT color scheme provided above (do not modify these colors)
- Create a marketable, professional design for digital publishing
- Follow {target_trend} design principles

Provide a complete design specification:
1. **trend**: "{target_trend}"
2. **concept_name**: Short catchy name for this design
3. **description**: 2-3 sentences describing the visual approach
4. **colors**: Use EXACTLY the colors provided above
5. **typography**: Font family suggestions and hierarchy
6. **visual_elements**: Specific shapes, patterns, or motifs for {target_trend} style
7. **mood**: Emotional tone that fits the style
8. **layout**: Description of text placement and visual balance
9. **accessibility**: Contrast ratio notes and readability considerations

FORMAT your response as VALID JSON only (no other text):
{{
  "trend": "{target_trend}",
  "concept_name": "Professional {book.cover_style.name} Design",
  "description": "A sophisticated design that captures the essence of {book.cover_style.name} style...",
  "colors": {{
    "primary": "{predefined_colors['primary']}",
    "secondary": "{predefined_colors['secondary']}", 
    "accent": "{predefined_colors['accent']}",
    "background": "{predefined_colors['background']}"
  }},
  "typography": "Clean sans-serif fonts with strong hierarchy",
  "visual_elements": "Geometric shapes and subtle patterns",
  "mood": "Professional and trustworthy",
  "layout": "Centered title with balanced visual elements",
  "accessibility": "High contrast text on light background"
}}

Remember:
- Use the REAL book title "{book.title}" in your description
- Make the design perfectly match {book.cover_style.name} style
- Use EXACTLY the colors provided (do not change them)
- Return ONLY valid JSON, no markdown code blocks or extra text
"""
        
        try:
            # Use Cloudflare AI instead of OpenRouter
            if self.cloudflare_client:
                print("🌩️  Using Cloudflare AI for cover style generation")
                system_prompt = "You are a creative book cover designer who creates professional covers matching specific design styles. Always respond with ONLY valid JSON, no markdown code blocks or extra text."
                full_prompt = f"{system_prompt}\n\n{prompt}"
                
                result = self.cloudflare_client.call_model(
                    prompt=full_prompt,
                    max_tokens=2000,
                    temperature=0.7
                )
                
                if not result.get('success'):
                    print(f"⚠️  Cloudflare AI failed: {result.get('error')}, using fallback")
                    return self._get_fallback_cover_concept(book)
                
                content = result.get('response', '')
                print(f"✓ Cloudflare AI response received ({len(content)} chars)")
            else:
                # No Cloudflare available, use fallback
                print("⚠️  No AI available, using fallback design")
                return self._get_fallback_cover_concept(book)
            
            # Clean up response
            content_clean = content.strip()
            if content_clean.startswith('```'):
                lines = content_clean.split('\n')
                content_clean = '\n'.join(lines[1:-1]) if len(lines) > 2 else content_clean
                content_clean = content_clean.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON response
            try:
                result = json.loads(content_clean)
                
                # FORCE the predefined colors to ensure visual distinction
                result['colors'] = predefined_colors
                
                print(f"Successfully parsed cover design for {book.cover_style.name} style")
                print(f"Applied colors: {predefined_colors}")
                return result
            
            except json.JSONDecodeError as je:
                print(f"Failed to parse JSON response: {je}")
                print(f"Raw response (first 500 chars): {content[:500]}")
                raise Exception("AI returned invalid JSON for cover design")
        
        except Exception as e:
            print(f"❌ Cover style concept generation error: {str(e)}")
            print("⚠️  Falling back to default cover design")
            return self._get_fallback_cover_concept(book)
    
    def _get_fallback_cover_concept(self, book) -> dict:
        """Return a simple fallback cover concept when AI is not available"""
        
        # Use predefined colors for the cover style
        style = book.cover_style.style if book.cover_style else 'minimalist'
        predefined_colors = self._get_style_color_schemes(style)
        
        return {
            'trend': 'minimalist_professional',
            'concept_name': f'Professional {book.cover_style.name if book.cover_style else "Clean"} Design',
            'description': f'A clean, professional cover for "{book.title}"',
            'colors': predefined_colors,
            'typography': 'Bold sans-serif title, clean subtitle',
            'visual_elements': 'Simple geometric shapes',
            'mood': 'Professional and trustworthy',
            'layout': 'Centered title with balanced spacing',
            'accessibility': 'High contrast AAA compliant'
        }
    
    def _create_simple_cover_pdf(self, title: str, concept: dict, pdf_path: str):
        """Create a simple ReportLab PDF cover based on the design concept"""
        
        try:
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            colors = concept.get('colors', {})
            bg_color = colors.get('background', '#ffffff')
            primary_color = colors.get('primary', '#000000')
            
            # Background
            if bg_color.startswith('#'):
                c.setFillColor(HexColor(bg_color))
            else:
                c.setFillColor(HexColor('#ffffff'))
            c.rect(0, 0, 8.5*inch, 11*inch, fill=1)
            
            # Title with smart wrapping
            if primary_color.startswith('#'):
                c.setFillColor(HexColor(primary_color))
            else:
                c.setFillColor(HexColor('#000000'))
            
            # Smart title wrapping based on character length and text width
            title_lines = self._smart_wrap_title(c, title, max_width=7*inch, font_name="Helvetica-Bold", initial_font_size=48)
            
            # Calculate optimal font size based on number of lines and content
            if len(title_lines) == 1:
                font_size = 48 if len(title_lines[0]) < 40 else 42
            elif len(title_lines) == 2:
                font_size = 40 if max(len(line) for line in title_lines) < 30 else 36
            else:
                font_size = 32
            
            # Draw title lines centered with proper spacing
            line_height = font_size * 1.2
            start_y = 6.5*inch if len(title_lines) <= 2 else 6.8*inch
            
            for i, line in enumerate(title_lines):
                c.setFont("Helvetica-Bold", font_size if i == 0 else font_size * 0.9)
                y_position = start_y - (i * line_height * 0.8)
                c.drawCentredString(4.25*inch, y_position, line)
            
            # Subtitle
            c.setFillColor(HexColor(colors.get('secondary', '#666666')))
            c.setFont("Helvetica", 24)
            c.drawCentredString(4.25*inch, 4.5*inch, "Professional Guide")
            
            c.save()
            print(f"✓ Simple cover PDF created: {pdf_path}")
            
        except Exception as e:
            print(f"Simple cover PDF creation error: {str(e)}")
            # Create fallback
            self._create_fallback_reportlab_cover(None, concept, pdf_path)
    
    def _get_modern_css(self) -> str:
        """Return modern CSS styles for PDF generation"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.4;
            color: #333;
        }
        
        .title {
            font-weight: 700;
            text-align: center;
        }
        
        .subtitle {
            font-weight: 300;
            text-align: center;
            text-transform: uppercase;
        }
        """