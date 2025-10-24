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
from .multi_llm_generator import MultiLLMOrchestrator
from .pdf_generator_pro import ProfessionalPDFGenerator
import logging


logger = logging.getLogger(__name__)


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
    Professional book generation using multiple LLMs
    """

    def __init__(self):
        try:
            self.llm_orchestrator = MultiLLMOrchestrator()
            self.llm_available = True
        except ValueError as e:
            print(f"Warning: {e}")
            self.llm_orchestrator = None
            self.llm_available = False

        self.pdf_generator = ProfessionalPDFGenerator()
    
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
    
    def generate_book_content(self, book):
        """Generate complete book content using multi-LLM strategy"""
        if not self.llm_available:
            raise Exception("LLM orchestrator not available - OPENROUTER_API_KEY not set")

        try:
            content_data = {}

            # 1. Generate Introduction (creative model)
            logger.info("Generating introduction...")
            intro_prompt = self._create_intro_prompt(book)
            content_data['introduction'] = self.llm_orchestrator.generate_with_fallback(
                prompt=intro_prompt,
                task_type='content_creative',
                max_tokens=1500
            )

            # Enhance introduction
            content_data['introduction'] = self.llm_orchestrator.enhance_content(
                content_data['introduction']
            )

            # 2. Generate Chapters (primary + technical models)
            chapters = []
            chapter_count = self._get_chapter_count(book.book_style)

            for i in range(chapter_count):
                logger.info(f"Generating chapter {i+1}/{chapter_count}...")
                chapter_title = self._generate_chapter_title(book, i)

                # Use primary model for main content
                chapter_content = self.llm_orchestrator.generate_chapter(
                    chapter_title=chapter_title,
                    context={
                        'book_title': book.title,
                        'domain': book.domain.name,
                        'niche': book.niche.name,
                        'audience': book.book_style.target_audience
                    },
                    word_count=1000  # Target 1000 words per chapter
                )

                # Validate and enhance if needed
                if len(chapter_content.split()) < 500:
                    logger.warning(f"Chapter {i+1} too short, enhancing...")
                    chapter_content = self.llm_orchestrator.enhance_content(chapter_content)

                chapters.append({
                    'title': chapter_title,
                    'content': chapter_content
                })

            content_data['chapters'] = chapters

            # 3. Generate Conclusion (creative model)
            logger.info("Generating conclusion...")
            conclusion_prompt = self._create_conclusion_prompt(book)
            content_data['conclusion'] = self.llm_orchestrator.generate_with_fallback(
                prompt=conclusion_prompt,
                task_type='content_creative',
                max_tokens=1200
            )

            # 4. Generate Takeaways (marketing model)
            logger.info("Generating actionable takeaways...")
            takeaways_prompt = self._create_takeaways_prompt(book)
            content_data['takeaways'] = self.llm_orchestrator.generate_with_fallback(
                prompt=takeaways_prompt,
                task_type='content_marketing',
                max_tokens=1000
            )

            return content_data

        except Exception as e:
            logger.error(f"Book content generation failed: {str(e)}")
            raise
    
    def _get_chapter_count(self, book_style) -> int:
        """Determine number of chapters based on book length"""
        if not book_style:
            return 5

        length_map = {
            'short': 4,   # 15-20 pages
            'medium': 6,  # 20-25 pages
            'full': 8     # 25-30 pages
        }

        return length_map.get(book_style.length, 5)
    
    def _create_intro_prompt(self, book) -> str:
        """Create prompt for introduction generation"""
        return f"""Write a compelling introduction for a professional book.

Book Title: {book.title}
Domain: {book.domain.name if book.domain else ''}
Niche: {book.niche.name if book.niche else ''}
Target Audience: {book.book_style.target_audience if book.book_style else 'professionals'}

Requirements:
1. Write 800-1000 words
2. Hook the reader in the first paragraph
3. Explain why this topic matters NOW (2025-2027 trends)
4. Outline what readers will learn
5. Use conversational yet professional tone
6. Include relevant statistics or market data
7. Create excitement and anticipation

Write a powerful introduction that makes readers eager to continue:"""

    def _create_conclusion_prompt(self, book) -> str:
        """Create prompt for conclusion generation"""
        return f"""Write a compelling conclusion for a professional book.

Book Title: {book.title}
Domain: {book.domain.name if book.domain else ''}
Niche: {book.niche.name if book.niche else ''}

Requirements:
1. Write 600-800 words
2. Summarize key insights and takeaways
3. Provide forward-looking perspective (2025-2027)
4. End with inspiring call to action
5. Reinforce the book's value proposition
6. Create lasting impact and motivation

Write a powerful conclusion that leaves readers transformed:"""

    def _create_takeaways_prompt(self, book) -> str:
        """Create prompt for actionable takeaways generation"""
        return f"""Create actionable takeaways section for a professional book.

Book Title: {book.title}
Domain: {book.domain.name if book.domain else ''}
Niche: {book.niche.name if book.niche else ''}

Requirements:
1. Write 400-600 words
2. List 8-12 specific, actionable steps
3. Focus on immediate implementation
4. Include measurable outcomes
5. Prioritize high-impact actions
6. Use clear, numbered format

Create practical takeaways that readers can implement immediately:"""

    def _generate_chapter_title(self, book, chapter_index: int) -> str:
        """Generate appropriate chapter title based on book content"""
        # This is a simplified version - in production you'd use AI to generate
        base_titles = [
            "Understanding the Fundamentals",
            "Building Strong Foundations",
            "Advanced Strategies and Techniques",
            "Real-World Applications",
            "Overcoming Common Challenges",
            "Future Trends and Innovations",
            "Implementation and Best Practices",
            "Measuring Success and ROI"
        ]

        if chapter_index < len(base_titles):
            return base_titles[chapter_index]
        else:
            return f"Chapter {chapter_index + 1}: Advanced Concepts"
    
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
    
    def create_pdf(self, book, content_data: Dict) -> str:
        """Create professional PDF"""
        output_filename = f"{self._clean_filename(book.title)}_interior.pdf"
        output_path = Path(settings.MEDIA_ROOT) / 'books' / output_filename

        self.pdf_generator.create_book_pdf(book, content_data, str(output_path))

        return str(output_path)
    
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
