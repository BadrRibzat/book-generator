# books/services/book_generator_new.py
"""
Professional Book Generator using OpenRouter DeepSeek R1T2 Chimera
Implements comprehensive prompts for 15-30 page professional books with 2025-2027 trends
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from .usage_tracker import UsageTracker
from .trending import get_trending_context, get_related_niches, format_trending_bullets


# Core AI Prompt for SmartBookForge
SMARTBOOK_AI_PROMPT = """
You are the AI engine of SmartBookForge, a SaaS platform that generates professional, on-demand PDF books with custom covers for two audiences: parents of preschoolers and digital marketers.

Follow this exact workflow:

1. AUDIENCE SELECTION:
Ask the user to choose between:
- Parents → Focus: early education, communication, curiosity, bedtime stories
- Digital Marketers → Focus: trending digital products (AI, sustainability, future skills, mental health tech)

2. DOMAIN/NICHE SELECTION:
Based on audience choice, present relevant domains and niches:
PARENTS: Bedtime Stories, Early Learning, Communication Skills, Emotional Development, Curiosity Building
DIGITAL MARKETERS: AI Content Creation, Sustainability Tech, Future Skills, Mental Health Tech, Digital Economy

3. BOOK LENGTH:
Offer: 15, 20, 25, or 30 pages

4. CONFIRMATION:
Summarize all choices and wait for user confirmation

5. BOOK GENERATION:
Once confirmed, generate:
- SEO-friendly title based on niche
- Book content: 60% practical + 40% foundational
- Structured: title, TOC, chapters, conclusion
- Clear, audience-appropriate language
- Output as clean, PDF-ready markdown

6. COVER PROMPTS:
Generate 3 cover design prompts for ReportLab-based PDF templates. Each must:
- Reference a domain-specific template (e.g., "AI Tech", "Mindful Parenting")
- Specify font, size, color, position for the book title overlay
- Describe layout using ReportLab terms: canvas, Drawing, Rect, HexColor, String, etc.
- Be labeled Cover A, Cover B, Cover C

Constraints:
- Use only OpenRouter DeepSeek R1T2 Chimera
- Never assume—always guide via explicit choices
- All output must integrate with Django + ReportLab + Celery

Current Request: {user_request}
Audience: {audience}
Niche: {niche}
Page Length: {page_length}

Generate the complete book with all sections.
"""


# Professional Book Prompt (15-30 pages minimum)
PROFESSIONAL_BOOK_PROMPT = """
System role:
You are a senior book author, instructional designer, and market strategist. You write authoritative, original books that blend credible research, practical frameworks, and clear structure. You adapt tone and pedagogy to the target audience and niche.

Project:
Create a comprehensive, engaging, and professionally structured book on the topic: "{sub_niche}"

Title:
- Generate a compelling, precise, and marketable book title that reflects the topic and audience. 
- Do NOT use placeholders like "Your Complete Guide".
- Title must be specific, benefit-driven, and memorable.

Audience and Tone:
- Primary audience: {audience}
- Tone: Professional yet accessible; practical and actionable; evidence-informed; inclusive and respectful.
- Voice: Expert but friendly, authoritative but approachable.

Structure (MINIMUM {page_length} pages):
- Front matter: Title, Subtitle, Short back-cover blurb (50–80 words), Table of Contents.
- Body: Introduction + 6-8 chapters (each with 3-5 subsections), Conclusion.
- End matter: Actionable Takeaways (bullet list), Glossary (10–20 key terms), Resources & Tools (curated links and references), Appendix with templates.
- Length: Aim for {page_length} pages of SUBSTANTIAL content. Each chapter should be 3-4 pages minimum.

Core Requirements:
- Research-backed insights (cite reputable sources: (Source: Organization, Year))
- Clear, step-by-step frameworks, checklists, and templates.
- Real-world case studies with measurable outcomes.
- Current market data points (timebox data to 2023-2025).
- Future outlook: 2025 and 2027 trend scenarios tied to the niche.
- Ethical use, accessibility, and inclusivity considerations.

Trending Niche Optimization:
{trending_context}

Related Topics to Consider:
{related_niches}

Kids & Family Safety Layer (apply if topic touches kids, preschool, family, or education):
- Age range: 3–6 (preschool) unless otherwise specified.
- Pedagogy: Play-based learning, short attention-span design, multisensory activities.
- Safety: Privacy-by-design, COPPA/GDPR-K awareness (practical guidance for parents/educators).
- Content style: Simple explanations, parent/educator notes, inclusive examples.
- Add "Bedtime-friendly" variants for stories and "Kitchen safety basics" for cooking content.
- Avoid medical claims; for skincare, emphasize gentle routines and dermatologist consultation.

Deliverables:
1) Title and Subtitle
2) Back-cover blurb
3) Table of Contents
4) Introduction (2-3 pages)
5) Chapters 1–8 with subsections (each chapter 3-4 pages)
6) Conclusion (2 pages)
7) Actionable Takeaways (1 page)
8) Glossary (15-20 terms)
9) Resources & Tools (include free AI tools relevant to the topic) (1 page)
10) Appendix with 2-3 templates or checklists (2 pages)

Formatting:
- Use clear headings and subheadings.
- Keep paragraphs concise; use bullet lists for frameworks and steps.
- Insert callout boxes like: **Note:**, **Caution:**, **Tip:** where helpful.
- Include specific examples, statistics, and actionable steps.

Constraints:
- Content must be original and not include copyrighted text.
- Keep statistics credible and avoid fabricated citations.
- If data is unknown, use ranges or industry-recognized estimates.
- MINIMUM {page_length} pages of content - do not write less.

Metadata for downstream services:
- Provide a one-line "Design Brief" summarizing visual motifs for the cover.

Now write the FULL BOOK per the above requirements. Make sure to write at least {page_length} pages of substantial, valuable content.
"""


class BookGeneratorProfessional:
    """
    Professional book generator using OpenRouter DeepSeek R1T2 Chimera
    Generates 15-30 page books with proper trending context and audience detection
    """
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in settings")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "deepseek/deepseek-chat"  # DeepSeek R1T2 Chimera
        self.usage_tracker = UsageTracker()
        self.media_root = Path(settings.MEDIA_ROOT)
        self.books_dir = self.media_root / 'books'
        self.books_dir.mkdir(parents=True, exist_ok=True)
    
    def infer_audience(self, book) -> str:
        """Detect audience based on book's niche and domain"""
        # Use the new model structure
        niche_name = book.niche.name.lower() if book.niche else ""
        domain_name = book.domain.name.lower() if book.domain else ""

        kids_signals = [
            'kids', 'preschool', 'family', 'bedtime', 'phonics', 'child',
            'children', 'parenting', 'education', 'learning', 'story'
        ]

        if any(sig in niche_name for sig in kids_signals) or any(sig in domain_name for sig in kids_signals):
            return "Parents, caregivers, and early educators"

        return "Modern professionals and lifelong learners"

    def design_brief_from_book(self, book) -> str:
        """Generate design brief based on book's domain and niche"""
        domain_name = book.domain.name.lower() if book.domain else ""
        niche_name = book.niche.name.lower() if book.niche else ""

        # Combine domain and niche for better design brief
        combined = f"{domain_name} {niche_name}".strip()

        if 'ai' in combined or 'digital' in combined or 'automation' in combined:
            return "Modern minimal, bold sans-serif, abstract neural motifs with subtle gradients, tech-forward aesthetic"

        if 'sustainability' in combined or 'eco' in combined or 'green' in combined or 'climate' in combined:
            return "Eco-modern, textured organic feel, leaf/earth abstracts, earthy greens with clean space, natural tones"

        if 'mental' in combined or 'mindfulness' in combined or 'wellness' in combined or 'stress' in combined:
            return "Calm editorial, soft gradients, high readability, soothing blues and lavenders, peaceful atmosphere"

        if 'kids' in combined or 'preschool' in combined or 'family' in combined or 'children' in combined:
            return "Playful, high-contrast shapes, friendly serif + rounded sans, warm pastels, child-friendly design"

        if 'startup' in combined or 'entrepreneurship' in combined or 'business' in combined:
            return "Editorial minimal, bold typography, geometric accents, professional confident aesthetic"

        if 'blockchain' in combined or 'crypto' in combined or 'metaverse' in combined or 'nft' in combined:
            return "Futuristic cyberpunk, neon accents, digital grid patterns, tech-forward dark themes"

        if 'remote' in combined or 'nomad' in combined or 'work' in combined:
            return "Clean modern, location-independent motifs, freedom themes, balanced professional aesthetic"

        return "Contemporary editorial minimalism with strong typographic hierarchy, professional and approachable"

    def build_book_prompt(self, book) -> str:
        """Build comprehensive prompt with trending context using new model structure"""
        # Use new model fields
        domain_name = book.domain.name if book.domain else "General"
        niche_name = book.niche.name if book.niche else "General Interest"
        audience = self.infer_audience(book)
        page_length = book.book_style.length if book.book_style else 'medium'

        # Get trending context based on niche
        trending_ctx = get_trending_context(niche_name)
        trending_text = format_trending_bullets(trending_ctx)

        # Get related niches
        related = get_related_niches(niche_name, limit=6)
        related_text = ', '.join([r.replace('_', ' ').title() for r in related]) if related else "Related professional development topics"

        return PROFESSIONAL_BOOK_PROMPT.format(
            sub_niche=f"{domain_name}: {niche_name}",
            audience=audience,
            page_length=page_length,
            trending_context=trending_text,
            related_niches=related_text
        )
    
    def call_openrouter_chat(self, messages: list, temperature: float = 0.7, max_tokens: int = 8000) -> Dict[str, Any]:
        """Call OpenRouter API with DeepSeek R1T2 Chimera"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://book-generator.com",
            "X-Title": "Professional Book Generator SaaS"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.9,
        }
        
        url = f"{self.base_url}/chat/completions"
        t0 = time.time()
        
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=180)  # 3 min timeout
            resp.raise_for_status()
            latency = time.time() - t0
            data = resp.json()
            
            # Track usage
            usage = data.get("usage", {})
            if usage:
                input_tokens = usage.get('prompt_tokens', 0)
                output_tokens = usage.get('completion_tokens', 0)
                self.usage_tracker.record_usage(input_tokens, output_tokens)
                print(f"API Usage: {input_tokens} prompt tokens, {output_tokens} completion tokens, {latency:.2f}s")
            
            return {"data": data, "usage": usage, "latency_sec": latency}
        
        except requests.exceptions.RequestException as e:
            print(f"OpenRouter API error: {str(e)}")
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    def generate_smartbook_content(self, book, audience: str = None, user_request: str = None) -> Dict[str, Any]:
        """Generate book content using SmartBookForge AI workflow"""
        
        # Determine audience if not provided
        if not audience:
            audience = self.infer_audience(book)
        
        # Use new model fields for the prompt
        domain_name = book.domain.name if book.domain else "General"
        niche_name = book.niche.name if book.niche else "General Interest"
        page_length = book.book_style.length if book.book_style else 'medium'

        # Build the SmartBook prompt
        prompt = SMARTBOOK_AI_PROMPT.format(
            user_request=user_request or f"Generate a {page_length}-page book about {domain_name}: {niche_name}",
            audience=audience,
            niche=f"{domain_name}: {niche_name}",
            page_length=page_length
        )
        
        system_msg = {
            "role": "system",
            "content": "You are the AI engine of SmartBookForge. Follow the exact workflow: guide user through audience selection, domain/niche choice, book length selection, confirmation, then generate complete book with cover prompts. Be interactive and never assume choices."
        }
        
        user_msg = {
            "role": "user",
            "content": prompt
        }
        
        print(f"Generating SmartBook content for: {domain_name} - {niche_name} ({page_length} pages) - Audience: {audience}")
        
        # Calculate required tokens
        required_tokens = int(self._get_page_count_from_length(page_length) * 650 * 1.5)
        max_tokens = max(required_tokens, 16000)
        
        print(f"Using max_tokens={max_tokens} for SmartBook generation")
        
        result = self.call_openrouter_chat(
            [system_msg, user_msg],
            temperature=0.7,
            max_tokens=max_tokens
        )
        
        content = result["data"]["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        
        # Parse the SmartBook response
        parsed_data = self.parse_smartbook_response(content, self._get_page_count_from_length(page_length))
        
        # Update book title if generated
        if parsed_data.get('title') and book.title in ["Untitled Book", "Generating..."]:
            book.title = parsed_data['title']
            book.save()
        
        return {
            "title": parsed_data.get('title', book.title),
            "content": content,
            "chapters": parsed_data.get("chapters", []),
            "cover_prompts": parsed_data.get("cover_prompts", []),
            "audience": audience,
            "usage": usage,
            "latency_sec": result["latency_sec"]
        }

    def _get_page_count_from_length(self, length: str) -> int:
        """Convert length string to page count"""
        length_map = {
            'short': 18,  # 15-20 pages
            'medium': 22,  # 20-25 pages
            'full': 27  # 25-30 pages
        }
        return length_map.get(length, 22)  # Default to medium
    
    def parse_smartbook_response(self, content: str, page_length: int) -> Dict[str, Any]:
        """Parse SmartBook AI response into structured data"""
        
        result = {
            'title': None,
            'chapters': [],
            'cover_prompts': []
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line_strip = line.strip()
            
            if not line_strip:
                continue
            
            # Extract title
            if not result['title'] and (line_strip.startswith('Title:') or line_strip.startswith('Book Title:')):
                result['title'] = line_strip.split(':', 1)[-1].strip()
                continue
            
            # Extract cover prompts
            if 'Cover A:' in line_strip or 'Cover B:' in line_strip or 'Cover C:' in line_strip:
                current_section = 'cover_prompts'
                result['cover_prompts'].append(line_strip)
                continue
            elif current_section == 'cover_prompts' and line_strip.startswith(('Cover ', 'Use ReportLab', 'Canvas', 'Title', 'Visual', 'ReportLab')):
                if result['cover_prompts']:
                    result['cover_prompts'][-1] += '\n' + line_strip
                continue
            
            # Extract chapters
            if line_strip.startswith('#') and ('Chapter' in line_strip or 'Introduction' in line_strip or 'Conclusion' in line_strip):
                current_section = 'chapters'
                result['chapters'].append({
                    'title': line_strip.lstrip('#').strip(),
                    'content': []
                })
                continue
            elif current_section == 'chapters' and result['chapters']:
                result['chapters'][-1]['content'].append(line)
        
        # Fallback parsing if structured parsing fails
        if not result['chapters']:
            result['chapters'] = self.parse_book_content(content, page_length).get('chapters', [])
        
        # Fallback cover prompts
        if not result['cover_prompts']:
            result['cover_prompts'] = self._get_fallback_cover_prompts(result.get('title', 'Professional Book'))
        
        return result
    
    def _get_fallback_cover_prompts(self, title: str) -> list:
        """Get fallback cover prompts if parsing fails"""
        return [
            f"Cover A: Modern Professional\nUse ReportLab canvas.drawString() to overlay '{title}' in Helvetica-Bold 48pt centered on a clean background.",
            f"Cover B: Elegant Typography\nUse ReportLab Paragraph with custom styles to render '{title}' with sophisticated typography.",
            f"Cover C: Bold Statement\nUse ReportLab canvas with high contrast colors to display '{title}' prominently."
        ]
    
    def generate_book_content(self, book):
        """Generate complete book content using OpenRouter"""
        prompt = self.build_book_prompt(book)
        
        system_msg = {
            "role": "system",
            "content": "You are a professional book author who creates comprehensive, valuable, and well-structured books. Follow instructions precisely and produce high-quality, original content with proper length and depth."
        }
        
        user_msg = {
            "role": "user",
            "content": prompt
        }
        
        # Use new model fields
        domain_name = book.domain.name if book.domain else "General"
        niche_name = book.niche.name if book.niche else "General Interest"
        page_length = self._get_page_count_from_length(book.book_style.length) if book.book_style else 22

        print(f"Generating book content for: {domain_name} - {niche_name} ({page_length} pages)")
        
        # Calculate required tokens based on page length
        # ~500 words per page, ~1.3 tokens per word = ~650 tokens per page
        # Add 50% buffer for formatting and structure
        required_tokens = int(page_length * 650 * 1.5)
        max_tokens = max(required_tokens, 16000)  # Minimum 16K tokens
        
        print(f"Using max_tokens={max_tokens} for {page_length} pages")
        
        result = self.call_openrouter_chat(
            [system_msg, user_msg],
            temperature=0.7,
            max_tokens=max_tokens
        )
        
        content = result["data"]["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        
        # Extract title and design brief
        title = self.extract_title(content) or self.generate_fallback_title(f"{domain_name} {niche_name}")
        design_brief = self.extract_design_brief(content) or self.design_brief_from_book(book)
        
        # Update book title if extracted (check for placeholder titles)
        if title and book.title in ["Untitled Book", "Generating..."]:
            book.title = title
            book.save()
        
        # Parse content into structured chapters
        parsed_content = self.parse_book_content(content, page_length)
        
        return {
            "title": title,
            "content": content,
            "chapters": parsed_content.get("chapters", []),
            "usage": usage,
            "latency_sec": result["latency_sec"],
            "design_brief": design_brief,
            "audience": self.infer_audience(book)
        }
    
    def extract_title(self, text: str) -> Optional[str]:
        """Extract title from generated content"""
        lines = text.split('\n')
        for i, line in enumerate(lines[:20]):  # Check first 20 lines
            ls = line.strip()
            
            # Look for explicit Title: marker (with markdown formatting)
            if 'title:' in ls.lower():
                # Check if title is on same line
                title = ls.split(':', 1)[1].strip()
                # Remove ALL markdown formatting recursively
                while any(char in title for char in ['*', '#', '_', '"', "'"]):
                    title = title.replace('**', '').replace('*', '').replace('__', '').replace('_', '').replace('#', '').replace('"', '').replace("'", '').strip()
                
                # If title is substantial, return it
                if title and len(title) > 10 and len(title) < 150:
                    return title
                
                # If title is empty or just whitespace, check next line
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    while any(char in next_line for char in ['*', '#', '_', '"', "'"]):
                        next_line = next_line.replace('**', '').replace('*', '').replace('__', '').replace('_', '').replace('#', '').replace('"', '').replace("'", '').strip()
                    if next_line and len(next_line) > 10 and len(next_line) < 150:
                        return next_line
            
            # Look for first substantial line that's not metadata
            if ls and len(ls) > 10 and len(ls) < 150:
                # Skip obvious non-titles
                if not any(skip in ls.lower() for skip in ['subtitle', 'table of contents', 'introduction', 'chapter', 'author', 'back-cover']):
                    # Clean up markdown formatting
                    title = ls.strip()
                    while any(char in title for char in ['*', '#', '_', '"', "'"]):
                        title = title.replace('**', '').replace('*', '').replace('__', '').replace('_', '').replace('#', '').replace('"', '').replace("'", '').strip()
                    if title and not title.startswith('---'):
                        return title
        
        return None
    
    def extract_design_brief(self, text: str) -> Optional[str]:
        """Extract design brief from generated content"""
        for line in reversed(text.split('\n')):
            if "Design Brief" in line or "design brief" in line:
                brief = line.split(":", 1)[-1].strip()
                if brief and len(brief) > 20:
                    return brief
        
        return None
    
    def generate_fallback_title(self, sub_niche: str) -> str:
        """Generate fallback title if extraction fails"""
        title_base = sub_niche.replace('_', ' ').title()
        return f"The {title_base} Handbook: Professional Guide for 2025"
    
    def clean_filename(self, name: str) -> str:
        """Clean title for filename"""
        # Remove special characters, keep alphanumeric, spaces, hyphens, underscores
        cleaned = ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_'))
        # Truncate if too long
        cleaned = cleaned[:100]
        # Replace multiple spaces with single underscore
        cleaned = '_'.join(cleaned.split())
        return cleaned or "Professional_Book"
    
    def parse_book_content(self, content: str, page_length: int) -> Dict[str, Any]:
        """Parse book content into structured chapters"""
        chapters = []
        current_chapter = None
        introduction = None
        conclusion = None
        actionable_takeaways = None
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line_strip = line.strip()
            
            # Skip empty lines in detection
            if not line_strip:
                continue
            
            # Detect sections
            line_upper = line_strip.upper()
            line_clean = line_strip.lstrip('#').strip().upper()  # Remove markdown headers
            
            if 'INTRODUCTION' in line_clean and len(line_clean) < 50:
                current_section = 'introduction'
                introduction = {'title': 'Introduction', 'content': []}
                continue
            
            elif 'CONCLUSION' in line_clean and len(line_clean) < 50:
                if current_chapter:
                    chapters.append(current_chapter)
                    current_chapter = None
                current_section = 'conclusion'
                conclusion = {'title': 'Conclusion', 'content': []}
                continue
            
            elif 'ACTIONABLE TAKEAWAYS' in line_clean or 'ACTION ITEMS' in line_clean:
                if current_chapter:
                    chapters.append(current_chapter)
                    current_chapter = None
                current_section = 'takeaways'
                actionable_takeaways = {'title': 'Actionable Takeaways', 'content': []}
                continue
            
            # Detect chapter headers (markdown ## or "Chapter X:" pattern)
            is_chapter = False
            chapter_title = None
            
            if line_strip.startswith('##') and not line_strip.startswith('###'):
                # Markdown level 2 header
                chapter_title = line_strip.lstrip('#').strip()
                is_chapter = True
            elif line_strip.startswith('CHAPTER ') or (line_strip.startswith('Chapter ') and ':' in line_strip):
                chapter_title = line_strip
                is_chapter = True
            elif line_clean.startswith('CHAPTER '):
                # Markdown formatted chapter
                chapter_title = line_strip.lstrip('#').strip().replace('**', '').strip()
                is_chapter = True
            
            if is_chapter:
                # Save previous chapter
                if current_chapter:
                    chapters.append(current_chapter)
                
                current_chapter = {'title': chapter_title, 'content': []}
                current_section = 'chapter'
                continue
            
            # Add content to appropriate section
            if current_section == 'introduction' and introduction:
                introduction['content'].append(line)
            elif current_section == 'conclusion' and conclusion:
                conclusion['content'].append(line)
            elif current_section == 'takeaways' and actionable_takeaways:
                actionable_takeaways['content'].append(line)
            elif current_section == 'chapter' and current_chapter:
                current_chapter['content'].append(line)
        
        # Add final chapter
        if current_chapter:
            chapters.append(current_chapter)
        
        # Structure response
        structured_content = []
        
        if introduction:
            structured_content.append(introduction)
        
        structured_content.extend(chapters)
        
        if conclusion:
            structured_content.append(conclusion)
        
        if actionable_takeaways:
            structured_content.append(actionable_takeaways)
        
        return {
            'chapters': structured_content,
            'total_chapters': len(structured_content),
            'structure': {
                'has_introduction': introduction is not None,
                'has_conclusion': conclusion is not None,
                'has_takeaways': actionable_takeaways is not None,
                'chapter_count': len(chapters)
            }
        }
    
    def create_pdf(self, book, content_data: Dict[str, Any]) -> str:
        """Create professional PDF with enhanced formatting"""
        # Use clean filename from book title
        clean_title = self.clean_filename(book.title)
        filename = f"{clean_title}_interior.pdf"
        pdf_path = self.books_dir / filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title=book.title,
            author="AI Book Generator Pro"
        )
        
        # Container for PDF elements
        story = []
        styles = getSampleStyleSheet()
        
        # Professional styles
        title_style = ParagraphStyle(
            'ProfessionalTitle',
            parent=styles['Heading1'],
            fontSize=32,
            textColor='#1a365d',
            spaceAfter=50,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=38
        )
        
        chapter_style = ParagraphStyle(
            'ChapterTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor='#2d3748',
            spaceAfter=30,
            spaceBefore=50,
            fontName='Helvetica-Bold',
            leading=26
        )
        
        section_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor='#4a5568',
            spaceAfter=18,
            spaceBefore=24,
            fontName='Helvetica-Bold',
            leading=20
        )
        
        body_style = ParagraphStyle(
            'ProfessionalBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=19,
            alignment=TA_JUSTIFY,
            spaceAfter=14,
            fontName='Helvetica',
            textColor='#2d3748'
        )
        
        # Title page
        story.append(Spacer(1, 3*inch))
        story.append(Paragraph(book.title, title_style))
        story.append(Spacer(1, 0.5*inch))
        story.append(PageBreak())
        
        # Table of contents
        toc_style = ParagraphStyle(
            'TOC',
            parent=styles['BodyText'],
            fontSize=12,
            leading=18,
            spaceAfter=10,
            fontName='Helvetica'
        )
        
        story.append(Paragraph("Table of Contents", chapter_style))
        story.append(Spacer(1, 0.4*inch))
        
        chapters_data = content_data.get('chapters', [])
        for i, chapter in enumerate(chapters_data, 1):
            toc_entry = f"{i}. {chapter.get('title', 'Chapter')}"
            story.append(Paragraph(toc_entry, toc_style))
        
        story.append(PageBreak())
        
        # Add chapters with enhanced formatting
        for chapter in chapters_data:
            # Chapter title
            story.append(Paragraph(chapter.get('title', 'Chapter'), chapter_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Chapter content
            for para in chapter.get('content', []):
                if para.strip():
                    # Detect subsection headings
                    if self.is_heading(para):
                        story.append(Paragraph(para.strip(), section_style))
                    else:
                        # Format body text
                        formatted_text = self.format_body_text(para)
                        if formatted_text:
                            story.append(Paragraph(formatted_text, body_style))
            
            story.append(PageBreak())
        
        # Build PDF
        try:
            doc.build(story)
            print(f"Successfully created PDF: {pdf_path}")
            return str(pdf_path)
        except Exception as e:
            print(f"PDF creation error: {str(e)}")
            raise Exception(f"Failed to create PDF: {str(e)}")
    
    def is_heading(self, text: str) -> bool:
        """Detect if text is a heading"""
        text_strip = text.strip()
        
        # Check for all caps short text
        if text_strip.isupper() and len(text_strip) < 100:
            return True
        
        # Check for numbered sections
        if text_strip and text_strip[0].isdigit() and text_strip[1:3] in ['. ', ') ']:
            return True
        
        # Check for specific heading markers
        heading_markers = ['Key Points:', 'Summary:', 'Action Steps:', 'Best Practices:', 'Tools:', 'Resources:']
        if any(marker.lower() in text_strip.lower() for marker in heading_markers):
            return True
        
        return False
    
    def format_body_text(self, text: str) -> str:
        """Format body text for professional appearance"""
        text = text.strip()
        
        # Remove excessive markdown
        text = text.replace('**', '').replace('*', '')
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Basic HTML escaping for ReportLab
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        return text


# Maintain backwards compatibility
BookGenerator = BookGeneratorProfessional
