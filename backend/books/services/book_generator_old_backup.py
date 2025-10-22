# books/services/book_generator.py
import os
import json
import requests
from pathlib import Path
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
from .usage_tracker import UsageTracker

class BookGenerator:
    """
    Generates complete book interior content using OpenRouter DeepSeek R1T2 Chimera
    Creates professional PDF with proper formatting and enhanced content quality
    """
    
    # Professional book titles optimized for market trends
    TITLE_TEMPLATES = {
        # AI & Digital Transformation
        'ai_productivity_tools': [
            'AI Productivity Revolution: Transform Your Workflow with Smart Tools',
            'The AI Productivity Blueprint: Master Tools That Work for You',
            'Smart Work Revolution: AI Tools for Maximum Productivity',
        ],
        'digital_nomad_guides': [
            'Digital Nomad Mastery: Build Freedom Through Remote Work',
            'Location Independence: The Complete Digital Nomad Guide',
            'Remote Work Revolution: Your Path to Digital Nomad Success',
        ],
        'automation_business': [
            'Business Automation Mastery: Scale with AI and Technology',
            'The Automation Blueprint: Transform Your Business Operations',
            'Smart Business Automation: Tools and Strategies for Growth',
        ],
        'chatgpt_prompts_mastery': [
            'ChatGPT Mastery: Advanced Prompt Engineering for Professionals',
            'The Prompt Engineering Blueprint: Master AI Communication',
            'AI Prompt Engineering: Unlock ChatGPT\'s Full Potential',
        ],
        'ai_content_creation': [
            'AI Content Creation Revolution: Generate, Optimize, Dominate',
            'The AI Content Blueprint: Master Digital Content Creation',
            'Content AI Mastery: Tools and Strategies for Creators',
        ],
        'remote_work_optimization': [
            'Remote Work Optimization: Thrive in the Digital Workplace',
            'The Remote Work Blueprint: Productivity and Balance',
            'Digital Workplace Mastery: Optimize Your Remote Work Life',
        ],
        
        # Sustainability & Green Tech
        'green_tech_startups': [
            'Green Tech Startup Revolution: Build Sustainable Businesses',
            'The Green Tech Blueprint: Innovation for a Better Planet',
            'Sustainable Startup Mastery: Green Technology Ventures',
        ],
        'sustainable_living': [
            'Sustainable Living Mastery: Your Complete Eco-Friendly Guide',
            'The Green Living Blueprint: Reduce, Reuse, Thrive',
            'Eco-Living Revolution: Sustainable Habits for Modern Life',
        ],
        'climate_tech': [
            'Climate Tech Innovation: Solutions for a Changing Planet',
            'The Climate Tech Blueprint: Technology Against Climate Change',
            'Climate Technology Mastery: Build Solutions That Matter',
        ],
        'eco_entrepreneurship': [
            'Eco-Entrepreneurship: Build Profitable Green Businesses',
            'The Green Business Blueprint: Sustainable Entrepreneurship',
            'Eco-Business Mastery: Profit with Purpose',
        ],
        'carbon_footprint_reduction': [
            'Carbon Footprint Mastery: Reduce Your Environmental Impact',
            'The Carbon Reduction Blueprint: Practical Climate Action',
            'Climate Action Guide: Minimize Your Carbon Footprint',
        ],
        
        # Mental Health Technology
        'digital_detox': [
            'Digital Detox Mastery: Reclaim Your Life from Technology',
            'The Digital Wellness Blueprint: Balance Tech and Life',
            'Tech-Life Balance: Master Digital Detox Strategies',
        ],
        'mindfulness_apps': [
            'Mindfulness Apps Revolution: Technology for Inner Peace',
            'The Digital Mindfulness Blueprint: Apps for Mental Wellness',
            'Mindful Tech: Apps and Tools for Mental Health',
        ],
        'mental_health_at_work': [
            'Workplace Mental Health: Technology Solutions for Well-being',
            'The Mental Health at Work Blueprint: Support Employee Wellness',
            'Corporate Wellness Tech: Mental Health in the Workplace',
        ],
        'stress_management_tech': [
            'Stress Management Technology: Digital Tools for Calm',
            'The Stress Tech Blueprint: Apps and Gadgets for Relaxation',
            'Digital Stress Relief: Technology for Mental Wellness',
        ],
        'sleep_optimization': [
            'Sleep Optimization Technology: Master Rest with Smart Tools',
            'The Sleep Tech Blueprint: Gadgets for Better Sleep',
            'Smart Sleep Solutions: Technology for Restful Nights',
        ],
        
        # Future Skills & Learning
        'prompt_engineering': [
            'Prompt Engineering Mastery: The Art of AI Communication',
            'The Prompt Engineering Blueprint: Master AI Interactions',
            'AI Communication: Advanced Prompt Engineering Techniques',
        ],
        'ai_ethics': [
            'AI Ethics Revolution: Responsible Artificial Intelligence',
            'The AI Ethics Blueprint: Navigate Technology\'s Moral Landscape',
            'Ethical AI Mastery: Responsible Technology Development',
        ],
        'digital_literacy': [
            'Digital Literacy Mastery: Essential Skills for the Modern World',
            'The Digital Skills Blueprint: Technology Proficiency Guide',
            'Tech Literacy Revolution: Master Digital Tools and Concepts',
        ],
        'remote_collaboration': [
            'Remote Collaboration Mastery: Tools and Strategies for Success',
            'The Remote Work Blueprint: Effective Virtual Teamwork',
            'Digital Collaboration: Tools for Remote Team Success',
        ],
        'future_job_skills': [
            'Future Job Skills: Prepare for Tomorrow\'s Workplace',
            'The Future Skills Blueprint: Essential Competencies for 2025',
            'Workforce of Tomorrow: Skills for Future Career Success',
        ],
    }
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "deepseek/deepseek-chat"  # DeepSeek R1T2 Chimera via OpenRouter
        self.usage_tracker = UsageTracker()
        self.media_root = Path(settings.MEDIA_ROOT)
        self.books_dir = self.media_root / 'books'
        self.books_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_title(self, sub_niche):
        """Generate optimized title for sub-niche"""
        titles = self.TITLE_TEMPLATES.get(sub_niche, ['Your Complete Guide'])
        return random.choice(titles)
    
    def generate_book_content(self, book):
        """
        Generate complete book content using OpenRouter DeepSeek R1T2 Chimera
        Returns dict with chapters and content
        """
        prompt = self._create_professional_prompt(book)
        
        try:
            # Make API call to OpenRouter
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://book-generator.com",
                    "X-Title": "Book Generator SaaS"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a professional book author and content strategist specializing in creating high-quality, publish-ready digital books. Write engaging, informative content that provides real value to readers with professional insights and actionable advice."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 8000,
                    "top_p": 0.9,
                },
                timeout=120  # 2 minute timeout for long content generation
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Track token usage
            if 'usage' in data:
                input_tokens = data['usage'].get('prompt_tokens', 0)
                output_tokens = data['usage'].get('completion_tokens', 0)
                self.usage_tracker.record_usage(input_tokens, output_tokens)
            
            content = data['choices'][0]['message']['content']
            return self._parse_book_content(content, book.page_length)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"OpenRouter API error: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Content generation failed: {str(e)}"
            print(error_msg)
            raise Exception(error_msg)
    
    def _create_professional_prompt(self, book):
        """Create professional prompt for high-quality book content generation"""
        
        # Get trending context based on sub_niche
        trending_context = self._get_trending_context(book.sub_niche)
        
        professional_prompt = f"""
You are a professional book author and content strategist. Create a comprehensive, engaging, and professionally structured book about: {book.sub_niche.replace('_', ' ').title()}

BOOK REQUIREMENTS:
- Target audience: Modern professionals and lifelong learners
- Tone: Professional yet accessible, actionable insights
- Structure: Introduction, 5-7 chapters, conclusion, actionable takeaways
- Style: Mix of research-backed insights and practical applications
- Length: {book.page_length} pages of substantial content

TRENDING ELEMENTS TO INCLUDE ({trending_context['year']}):
- Current market trends and statistics
- Real-world case studies from {trending_context['industry']}
- Actionable frameworks and templates
- Future predictions and opportunities
- Resource recommendations

CONTENT STRUCTURE:
1. Introduction (2-3 pages)
   - Hook with compelling statistic or story
   - Overview of the {book.sub_niche.replace('_', ' ')} landscape
   - What readers will learn
   - Target audience benefits

2. Core Chapters (4-5 chapters, 3-4 pages each)
   - Chapter 1: Foundation and Fundamentals
   - Chapter 2: Current Trends and Best Practices
   - Chapter 3: Practical Implementation Strategies
   - Chapter 4: Advanced Techniques and Case Studies
   - Chapter 5: Future Outlook and Innovation

3. Conclusion (1-2 pages)
   - Key takeaways summary
   - Action plan for implementation
   - Resources for continued learning

4. Actionable Takeaways
   - Step-by-step implementation guide
   - Common pitfalls to avoid
   - Success metrics and measurement

Ensure the content is original, valuable, and positions the reader as an informed expert in this niche.

FORMAT your response as:

INTRODUCTION
[Compelling introduction content]

CHAPTER 1: [Title]
[Professional chapter content with actionable insights]

CHAPTER 2: [Title]
[Chapter content]

... continue for all chapters

CONCLUSION
[Strong conclusion with takeaways]

ACTIONABLE TAKEAWAYS
[Practical implementation steps]
"""
        return professional_prompt
    
    def _get_trending_context(self, sub_niche):
        """Get trending context for different niches"""
        trending_data = {
            # AI & Digital Transformation
            'ai_productivity_tools': {
                'year': '2024-2025',
                'industry': 'AI productivity software companies',
                'trends': ['AI automation', 'workflow optimization', 'smart assistants']
            },
            'digital_nomad_guides': {
                'year': '2024-2025', 
                'industry': 'remote work technology',
                'trends': ['hybrid work models', 'digital collaboration', 'work-life balance']
            },
            'automation_business': {
                'year': '2024-2025',
                'industry': 'business process automation',
                'trends': ['RPA', 'AI workflow automation', 'process optimization']
            },
            'chatgpt_prompts_mastery': {
                'year': '2024-2025',
                'industry': 'AI prompt engineering',
                'trends': ['advanced prompting', 'AI-human collaboration', 'custom GPTs']
            },
            'ai_content_creation': {
                'year': '2024-2025',
                'industry': 'AI content tools',
                'trends': ['generative AI', 'content automation', 'personalized marketing']
            },
            'remote_work_optimization': {
                'year': '2024-2025',
                'industry': 'remote work solutions',
                'trends': ['async communication', 'virtual collaboration', 'productivity metrics']
            },
            
            # Sustainability & Green Tech
            'green_tech_startups': {
                'year': '2024-2025',
                'industry': 'clean technology',
                'trends': ['renewable energy', 'carbon capture', 'sustainable materials']
            },
            'sustainable_living': {
                'year': '2024-2025',
                'industry': 'eco-friendly products',
                'trends': ['circular economy', 'zero waste', 'sustainable consumption']
            },
            'climate_tech': {
                'year': '2024-2025',
                'industry': 'climate technology',
                'trends': ['carbon reduction', 'climate adaptation', 'green innovation']
            },
            'eco_entrepreneurship': {
                'year': '2024-2025',
                'industry': 'green business',
                'trends': ['impact investing', 'sustainable business models', 'B Corp movement']
            },
            'carbon_footprint_reduction': {
                'year': '2024-2025',
                'industry': 'carbon management',
                'trends': ['carbon accounting', 'offset programs', 'net-zero strategies']
            },
            
            # Mental Health Technology
            'digital_detox': {
                'year': '2024-2025',
                'industry': 'digital wellness',
                'trends': ['screen time management', 'mindful technology use', 'digital balance']
            },
            'mindfulness_apps': {
                'year': '2024-2025',
                'industry': 'mental health technology',
                'trends': ['meditation apps', 'mental health tracking', 'digital therapeutics']
            },
            'mental_health_at_work': {
                'year': '2024-2025',
                'industry': 'workplace wellness',
                'trends': ['employee mental health', 'workplace culture', 'stress management']
            },
            'stress_management_tech': {
                'year': '2024-2025',
                'industry': 'stress reduction technology',
                'trends': ['biofeedback', 'wearable stress monitors', 'relaxation apps']
            },
            'sleep_optimization': {
                'year': '2024-2025',
                'industry': 'sleep technology',
                'trends': ['sleep tracking', 'smart sleep aids', 'circadian rhythm optimization']
            },
            
            # Future Skills & Learning
            'prompt_engineering': {
                'year': '2024-2025',
                'industry': 'AI education',
                'trends': ['AI literacy', 'prompt design', 'human-AI interaction']
            },
            'ai_ethics': {
                'year': '2024-2025',
                'industry': 'AI governance',
                'trends': ['responsible AI', 'AI bias mitigation', 'ethical frameworks']
            },
            'digital_literacy': {
                'year': '2024-2025',
                'industry': 'digital education',
                'trends': ['online learning', 'digital skills', 'technology adaptation']
            },
            'remote_collaboration': {
                'year': '2024-2025',
                'industry': 'collaboration technology',
                'trends': ['virtual teams', 'async communication', 'global collaboration']
            },
            'future_job_skills': {
                'year': '2024-2025',
                'industry': 'workforce development',
                'trends': ['emerging skills', 'career transition', 'lifelong learning']
            },
        }
        
        return trending_data.get(sub_niche, {
            'year': '2024-2025',
            'industry': 'modern professional development',
            'trends': ['innovation', 'digital transformation', 'professional growth']
        })
    
    def _parse_book_content(self, content, page_length):
        """Parse professional book content into structured format"""
        chapters = []
        current_chapter = None
        introduction = None
        conclusion = None
        actionable_takeaways = None
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Handle different sections
            if line.upper() == 'INTRODUCTION':
                current_section = 'introduction'
                introduction = {'title': 'Introduction', 'content': []}
                continue
            elif line.upper() == 'CONCLUSION':
                current_section = 'conclusion'
                conclusion = {'title': 'Conclusion', 'content': []}
                continue
            elif 'ACTIONABLE TAKEAWAYS' in line.upper():
                current_section = 'takeaways'
                actionable_takeaways = {'title': 'Actionable Takeaways', 'content': []}
                continue
            elif line.startswith('CHAPTER ') or ('CHAPTER ' in line.upper() and ':' in line):
                # Save previous chapter if exists
                if current_chapter:
                    chapters.append(current_chapter)
                
                # Clean up the title
                title = line.replace('**', '').replace(':', '').strip()
                current_chapter = {
                    'title': title,
                    'content': []
                }
                current_section = 'chapter'
                continue
            
            # Add content to appropriate section
            if current_section == 'introduction' and introduction and line:
                introduction['content'].append(line)
            elif current_section == 'conclusion' and conclusion and line:
                conclusion['content'].append(line)
            elif current_section == 'takeaways' and actionable_takeaways and line:
                actionable_takeaways['content'].append(line)
            elif current_section == 'chapter' and current_chapter and line:
                current_chapter['content'].append(line)
        
        # Add final chapter
        if current_chapter:
            chapters.append(current_chapter)
        
        # Structure the response
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
    
    def create_pdf(self, book, content_data):
        """
        Create professional PDF from book content with enhanced formatting
        Returns path to generated PDF
        """
        filename = f"book_{book.id}_interior.pdf"
        pdf_path = self.books_dir / filename
        
        # Create PDF document with professional settings
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title=book.title,
            author="AI Book Generator"
        )
        
        # Container for PDF elements
        story = []
        styles = getSampleStyleSheet()
        
        # Enhanced professional styles
        title_style = ParagraphStyle(
            'ProfessionalTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor='#1a365d',
            spaceAfter=40,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=32
        )
        
        chapter_style = ParagraphStyle(
            'ChapterTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor='#2d3748',
            spaceAfter=25,
            spaceBefore=40,
            fontName='Helvetica-Bold',
            leading=24
        )
        
        section_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor='#4a5568',
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            leading=20
        )
        
        body_style = ParagraphStyle(
            'ProfessionalBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=18,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontName='Helvetica',
            textColor='#2d3748'
        )
        
        # Add title page
        story.append(Spacer(1, 3*inch))
        story.append(Paragraph(book.title, title_style))
        story.append(Spacer(1, 0.5*inch))
        story.append(PageBreak())
        
        # Add table of contents
        toc_style = ParagraphStyle(
            'TOC',
            parent=styles['BodyText'],
            fontSize=12,
            leading=16,
            spaceAfter=8,
            fontName='Helvetica'
        )
        
        story.append(Paragraph("Table of Contents", chapter_style))
        story.append(Spacer(1, 0.3*inch))
        
        for i, chapter in enumerate(content_data['chapters'], 1):
            toc_entry = f"{i}. {chapter['title']}"
            story.append(Paragraph(toc_entry, toc_style))
        
        story.append(PageBreak())
        
        # Add chapters with professional formatting
        for chapter in content_data['chapters']:
            # Chapter title
            story.append(Paragraph(chapter['title'], chapter_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Chapter content with enhanced formatting
            for paragraph in chapter['content']:
                if paragraph:
                    # Detect headings (all caps, numbered sections, or specific patterns)
                    if (paragraph.isupper() and len(paragraph) < 80) or \
                       (paragraph[0].isdigit() and paragraph[1:3] in ['. ', ') ']) or \
                       any(phrase in paragraph.lower() for phrase in ['key points:', 'summary:', 'action steps:']):
                        story.append(Paragraph(paragraph, section_style))
                    else:
                        # Clean up and format body text
                        formatted_text = self._format_body_text(paragraph)
                        story.append(Paragraph(formatted_text, body_style))
            
            story.append(PageBreak())
        
        # Build PDF with error handling
        try:
            doc.build(story)
            print(f"Successfully created professional PDF: {pdf_path}")
            return str(pdf_path)
        except Exception as e:
            print(f"PDF creation error: {str(e)}")
            raise Exception(f"Failed to create PDF: {str(e)}")
    
    def _format_body_text(self, text):
        """Format body text for professional appearance"""
        # Clean up common formatting issues
        text = text.strip()
        
        # Remove excessive asterisks or markdown
        text = text.replace('**', '').replace('*', '')
        
        # Ensure proper spacing
        text = ' '.join(text.split())
        
        return text
