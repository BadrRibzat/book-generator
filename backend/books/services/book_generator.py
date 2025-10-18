# books/services/book_generator.py
import os
from pathlib import Path
from django.conf import settings
from groq import Groq
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random

class BookGenerator:
    """
    Generates complete book interior content using Groq LLM
    Creates professional PDF with proper formatting
    """
    
    # Market-optimized, non-editable titles for each sub-niche
    TITLE_TEMPLATES = {
        # Language and Kids
        'ai_learning_stories': [
            '[Child\'s Name]\'s First Adventure: Learning Spanish with Paco the Parrot',
            'Personalized Learning Tales: Your Child\'s Language Journey',
            'AI-Powered Stories: Custom Language Adventures for Kids',
        ],
        'multilingual_coloring': [
            'My First Bilingual ABCs: An English and French Coloring Book',
            'Color & Learn: Multilingual Fun for Little Ones',
            'Bilingual Coloring Adventures: Learn While You Color',
        ],
        'kids_mindful_journals': [
            'My Feelings Journal: A Kid\'s Guide to Understanding Big Emotions',
            'The Mindful Kid: Daily Activities for Emotional Wellness',
            'Big Feelings, Little Hands: A Child\'s Mindfulness Journal',
        ],
        
        # Technology and AI
        'ai_ethics': [
            'Generative AI: Creating Content in 2025 and Beyond',
            'AI Ethics Explained: Navigating the Future Responsibly',
            'The Ethical AI Handbook: A Professional\'s Guide',
        ],
        'nocode_guides': [
            'Build Your First App: A No-Code Manual for Creatives',
            'No-Code Revolution: Create Software Without Programming',
            'Low-Code Development Made Simple: For Beginners',
        ],
        'smart_home_diy': [
            'Your Automated Home: A Beginner\'s Guide to HomeKit and Google Home',
            'Smart Home Setup: DIY Automation for Everyone',
            'The Complete Smart Home Manual: Step-by-Step Guide',
        ],
        
        # Nutrition and Wellness
        'specialty_diet': [
            'The 2025 Keto Diet Air Fryer Cookbook for Beginners',
            'Specialty Diet Success: Custom Meal Plans for Your Lifestyle',
            'Dietary Freedom: Delicious Recipes for Every Need',
        ],
        'plant_based_cooking': [
            'The 30-Day Vegan: Simple, Plant-Based Recipes for Beginners',
            'Plant-Powered Cooking: Easy Vegan Meals',
            'Beginner\'s Guide to Plant-Based Living',
        ],
        'nutrition_mental_health': [
            'Eating for Happiness: A Guide to Mood-Boosting Foods',
            'The Mind-Gut Connection: Nutrition for Mental Wellness',
            'Food & Mood: How Diet Impacts Your Mental Health',
        ],
        
        # Meditation
        'mindfulness_anxiety': [
            'Anxiety Release: A 30-Day Mindfulness Workbook',
            'Calm Mind, Happy Life: Practical Anxiety Relief',
            'The Mindfulness Solution for Anxiety',
        ],
        'sleep_meditation': [
            'Journey Through the Sleepy Forest: A Guided Meditation Book',
            'Restful Nights: Sleep Meditation Stories',
            'Bedtime Calm: Guided Stories for Deep Sleep',
        ],
        'gratitude_journals': [
            'My Daily Gratitude Practice: 365 Days of Mindful Prompts',
            'The Gratitude Journal: Daily Reflections for Joy',
            'Thankful Every Day: A Year of Gratitude',
        ],
        
        # Home Workout
        'equipment_free': [
            '20-Minute Bodyweight Workouts: High-Intensity Training at Home',
            'No Equipment Needed: Complete Home Fitness Guide',
            'Bodyweight Mastery: Get Fit Anywhere',
        ],
        'yoga_remote_workers': [
            'Desk Stretch: A Yoga Guide for Relieving Pain and Tension at Your Desk',
            'The Remote Worker\'s Yoga Manual',
            'Office Yoga: Stay Flexible While Working',
        ],
        'mobility_training': [
            'Unlock Your Body: A Beginner\'s Guide to Mobility and Flexibility',
            'Mobility First: Easy Exercises for Better Movement',
            'The Flexibility Blueprint: Improve Range of Motion',
        ],
    }
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.media_root = Path(settings.MEDIA_ROOT)
        self.books_dir = self.media_root / 'books'
        self.books_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_title(self, sub_niche):
        """Generate optimized title for sub-niche"""
        titles = self.TITLE_TEMPLATES.get(sub_niche, ['Your Complete Guide'])
        return random.choice(titles)
    
    def generate_book_content(self, book):
        """
        Generate complete book content using Groq LLM
        Returns dict with chapters and content
        """
        prompt = self._create_generation_prompt(book)
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast, available model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional book writer specializing in creating high-quality, publish-ready digital books. Write engaging, informative content that provides real value to readers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=8000,
                top_p=0.9,
            )
            
            content = response.choices[0].message.content
            return self._parse_book_content(content, book.page_length)
            
        except Exception as e:
            raise Exception(f"Failed to generate book content: {str(e)}")
    
    def _create_generation_prompt(self, book):
        """Create detailed prompt for LLM"""
        niche_context = {
            'yoga_beginners': 'beginner-friendly yoga poses, breathing techniques, and getting started tips',
            'home_workouts': 'effective home exercises, workout routines, and equipment-free fitness',
            'mental_wellness': 'mental health practices, mindfulness, stress management, and emotional well-being',
            'vegan_recipes': 'plant-based recipes, nutrition tips, and cooking techniques',
            'meal_prep': 'meal planning strategies, batch cooking, and healthy eating habits',
            'smoothie_recipes': 'nutritious smoothie recipes, ingredient combinations, and health benefits',
            'productivity': 'productivity systems, time management, and efficiency hacks',
            'morning_routines': 'morning habits, routines of successful people, and starting the day right',
            'goal_setting': 'goal-setting frameworks, achievement strategies, and motivation techniques',
            'gardening': 'home gardening basics, plant care, and growing your own food',
            'photography': 'photography basics, camera settings, composition, and lighting',
            'diy_crafts': 'DIY project ideas, crafting techniques, and creative home decor',
            'minimalism': 'minimalist lifestyle, decluttering, and intentional living',
            'sustainable_living': 'eco-friendly practices, reducing waste, and green living',
            'travel_hacks': 'travel tips, budget travel, and destination guides',
        }
        
        context = niche_context.get(book.sub_niche, 'practical tips and advice')
        
        return f"""
Write a complete {book.page_length}-page digital book titled "{book.title}".

TOPIC: {context}

REQUIREMENTS:
- Create {book.page_length // 5} main chapters (each 4-6 pages when formatted)
- Each chapter should have:
  * Engaging chapter title
  * Introduction paragraph
  * 3-5 main sections with subheadings
  * Practical tips, examples, or action steps
  * Brief conclusion
- Write in a conversational yet professional tone
- Include actionable advice readers can implement immediately
- Use clear, concise language
- Make it valuable and publish-ready

FORMAT your response as:

CHAPTER 1: [Title]
[Content with clear sections and subheadings]

CHAPTER 2: [Title]
[Content]

... continue for all chapters

Make this a book people would actually want to read and implement. Focus on practical value.
"""
    
    def _parse_book_content(self, content, page_length):
        """Parse LLM output into structured format"""
        chapters = []
        current_chapter = None
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('CHAPTER '):
                if current_chapter:
                    chapters.append(current_chapter)
                current_chapter = {
                    'title': line,
                    'content': []
                }
            elif current_chapter and line:
                current_chapter['content'].append(line)
        
        if current_chapter:
            chapters.append(current_chapter)
        
        return {
            'chapters': chapters,
            'total_chapters': len(chapters)
        }
    
    def create_pdf(self, book, content_data):
        """
        Create formatted PDF from book content
        Returns path to generated PDF
        """
        filename = f"book_{book.id}_interior.pdf"
        pdf_path = self.books_dir / filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container for PDF elements
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2C3E50',
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        chapter_style = ParagraphStyle(
            'ChapterTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor='#34495E',
            spaceAfter=20,
            spaceBefore=30,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='#2C3E50',
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontName='Helvetica'
        )
        
        # Title page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph(book.title, title_style))
        story.append(Spacer(1, 0.5*inch))
        story.append(PageBreak())
        
        # Add chapters
        for chapter in content_data['chapters']:
            # Chapter title
            story.append(Paragraph(chapter['title'], chapter_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Chapter content
            for paragraph in chapter['content']:
                if paragraph:
                    # Detect if it's a heading (all caps or starts with number)
                    if paragraph.isupper() or (len(paragraph) < 60 and ':' in paragraph):
                        story.append(Paragraph(paragraph, heading_style))
                    else:
                        story.append(Paragraph(paragraph, body_style))
            
            story.append(PageBreak())
        
        # Build PDF
        doc.build(story)
        
        return str(pdf_path)
