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
        # Personal Development
        'productivity_home': [
            'Boost Your Home Office Productivity: A Complete Guide',
            'Work From Home Success: Productivity Strategies That Work',
            'Home Office Mastery: Stay Productive and Focused',
        ],
        'self_esteem': [
            'Build Unstoppable Self-Esteem: Your Confidence Blueprint',
            'The Self-Esteem Revolution: Transform Your Self-Image',
            'Confidence Unleashed: Master Your Self-Esteem',
        ],
        'parenting_guidance': [
            'Modern Parenting Mastery: Raise Confident Kids',
            'The Ultimate Parenting Guide for Today\'s World',
            'Parenting with Purpose: Guide Your Children to Success',
        ],
        'mental_health': [
            'Mental Health Mastery: Take Control of Your Mind',
            'The Mental Wellness Blueprint: Your Path to Inner Peace',
            'Mind Matters: Essential Mental Health Strategies',
        ],
        
        # Business & Entrepreneurship
        'online_business': [
            'Start Your Online Empire: The Complete Business Guide',
            'Online Business Success: From Idea to Profit',
            'Digital Entrepreneurship: Build Your Online Business',
        ],
        'investing_basics': [
            'Investing for Beginners: Your Wealth Building Guide',
            'The Investment Blueprint: Start Building Wealth Today',
            'Smart Investing: Master the Basics of Wealth Creation',
        ],
        'marketing_guide': [
            'Digital Marketing Mastery: Grow Your Business Online',
            'Marketing Magic: Strategies That Drive Results',
            'The Marketing Playbook: Win in the Digital Age',
        ],
        'business_planning': [
            'Business Planning Excellence: Your Success Roadmap',
            'Strategic Business Planning: Build a Winning Company',
            'The Business Plan Blueprint: Plan Your Path to Success',
        ],
        
        # Health & Wellness
        'general_health': [
            'Total Health Transformation: Your Wellness Journey',
            'The Complete Health Guide: Body, Mind, and Spirit',
            'Holistic Health Mastery: Optimize Your Well-Being',
        ],
        'autoimmune_living': [
            'Autoimmune Wellness: Thrive with Autoimmune Conditions',
            'Living Well with Autoimmunity: Your Complete Guide',
            'Autoimmune Living Mastery: Health and Happiness',
        ],
        'holistic_wellness': [
            'Holistic Wellness Revolution: Transform Your Health',
            'The Holistic Health Handbook: Natural Wellness Solutions',
            'Complete Wellness: Body, Mind, and Spirit Harmony',
        ],
        'fitness_nutrition': [
            'Fitness & Nutrition Mastery: Your Complete Guide',
            'The Fitness Nutrition Blueprint: Build Your Best Body',
            'Fit & Fueled: Nutrition Strategies for Peak Performance',
        ],
        
        # Relationships
        'dating_advice': [
            'Modern Dating Mastery: Find Love in Today\'s World',
            'The Dating Success Blueprint: Attract Your Perfect Match',
            'Love in the Digital Age: Modern Dating Strategies',
        ],
        'marriage_tips': [
            'Marriage Mastery: Build a Lasting, Loving Relationship',
            'The Marriage Success Guide: Strengthen Your Bond',
            'Forever Love: Secrets to a Happy Marriage',
        ],
        'conflict_resolution': [
            'Conflict Resolution Mastery: Transform Relationship Challenges',
            'The Peace Maker\'s Guide: Resolve Conflicts Effectively',
            'Relationship Harmony: Master Conflict Resolution',
        ],
        'communication_skills': [
            'Communication Excellence: Master the Art of Connection',
            'The Communication Blueprint: Speak with Confidence',
            'Effective Communication: Transform Your Relationships',
        ],
        
        # Children's Books
        'early_readers': [
            'Adventure Stories for Young Readers: Spark Imagination',
            'Fun Tales for Early Readers: Learning Through Stories',
            'Young Reader Adventures: Stories That Inspire',
        ],
        'religion_manners': [
            'Good Manners & Values: Stories for Children',
            'Character Building Stories: Manners and Morality',
            'Moral Tales for Kids: Lessons in Goodness',
        ],
        'educational_fun': [
            'Learning Adventures: Fun Educational Stories for Kids',
            'Educational Fun: Stories That Teach and Entertain',
            'Smart Kids Stories: Learning Through Play',
        ],
        'bedtime_stories': [
            'Magical Bedtime Stories: Sweet Dreams for Children',
            'Bedtime Tales: Stories for Peaceful Sleep',
            'Dreamland Stories: Bedtime Adventures for Kids',
        ],
        
        # Education & Learning
        'study_techniques': [
            'Study Smart: Master Effective Learning Techniques',
            'The Study Success Blueprint: Ace Your Exams',
            'Learning Mastery: Study Techniques That Work',
        ],
        'exam_preparation': [
            'Exam Success Mastery: Prepare, Perform, Excel',
            'The Exam Preparation Guide: Your Path to Success',
            'Test Taking Excellence: Master Exam Strategies',
        ],
        'language_learning': [
            'Language Learning Mastery: Speak Any Language Fluently',
            'The Language Learning Blueprint: Fast Track to Fluency',
            'Master Any Language: Proven Learning Strategies',
        ],
        'online_learning': [
            'Online Learning Excellence: Master Digital Education',
            'The Online Learning Guide: Succeed in Virtual Education',
            'Digital Learning Mastery: Thrive in Online Courses',
        ],
        
        # Technology & Digital Skills
        'coding_basics': [
            'Coding for Beginners: Your Programming Journey Starts Here',
            'The Coding Blueprint: Learn to Code from Scratch',
            'Programming Mastery: From Beginner to Developer',
        ],
        'graphic_design': [
            'Graphic Design Mastery: Create Stunning Visuals',
            'The Design Blueprint: Master Graphic Design Skills',
            'Visual Design Excellence: From Concept to Creation',
        ],
        'social_media_marketing': [
            'Social Media Marketing Mastery: Grow Your Brand Online',
            'The Social Media Blueprint: Dominate Digital Marketing',
            'Social Success: Marketing Strategies That Work',
        ],
        'digital_tools': [
            'Digital Tools Mastery: Boost Productivity with Technology',
            'The Digital Tools Guide: Essential Software for Success',
            'Tech Productivity: Master Digital Tools and Apps',
        ],
        
        # Finance & Investment
        'personal_finance': [
            'Personal Finance Mastery: Take Control of Your Money',
            'The Money Management Blueprint: Build Wealth Wisely',
            'Financial Freedom: Master Personal Finance Skills',
        ],
        'investment_strategies': [
            'Investment Mastery: Strategies for Wealth Creation',
            'The Investment Guide: Build Your Financial Future',
            'Smart Investing: Proven Strategies for Success',
        ],
        'retirement_planning': [
            'Retirement Planning Mastery: Secure Your Golden Years',
            'The Retirement Blueprint: Plan for Financial Freedom',
            'Retirement Success: Your Complete Planning Guide',
        ],
        'financial_independence': [
            'Financial Independence Mastery: Escape the Rat Race',
            'The FI Blueprint: Achieve Financial Freedom',
            'Wealth Building Mastery: Path to Financial Independence',
        ],
        
        # Hobbies & Interests
        'cooking_recipes': [
            'Culinary Mastery: Recipes and Techniques for Home Cooks',
            'The Cooking Blueprint: Master Kitchen Skills',
            'Cooking Excellence: From Beginner to Gourmet Chef',
        ],
        'diy_crafts': [
            'DIY Crafts Mastery: Create Beautiful Handmade Items',
            'The Crafting Blueprint: Handmade Projects for Everyone',
            'Crafting Excellence: DIY Projects That Inspire',
        ],
        'gardening_guide': [
            'Gardening Mastery: Grow Your Own Food and Flowers',
            'The Gardening Blueprint: Create Your Dream Garden',
            'Green Thumb Success: Master Gardening Skills',
        ],
        'photography_tips': [
            'Photography Mastery: Capture Stunning Images',
            'The Photography Blueprint: From Snapshots to Art',
            'Photo Excellence: Master the Art of Photography',
        ],
        
        # Travel & Adventure
        'travel_guides': [
            'Travel Mastery: Explore the World Like a Pro',
            'The Travel Blueprint: Plan Perfect Adventures',
            'Wanderlust: Your Ultimate Travel Guide',
        ],
        'budget_travel': [
            'Budget Travel Mastery: Travel the World on a Budget',
            'The Budget Travel Blueprint: Affordable Adventures',
            'Smart Travel: Save Money, See the World',
        ],
        'adventure_planning': [
            'Adventure Planning Mastery: Create Unforgettable Experiences',
            'The Adventure Blueprint: Plan Epic Journeys',
            'Adventure Excellence: Master Trip Planning Skills',
        ],
        'cultural_exploration': [
            'Cultural Exploration Mastery: Discover World Cultures',
            'The Culture Blueprint: Immerse Yourself in Global Traditions',
            'Cultural Journeys: Explore Diverse Cultures and Customs',
        ],
        
        # Productivity & Time Management
        'time_management': [
            'Time Management Mastery: Make Every Minute Count',
            'The Productivity Blueprint: Master Your Time',
            'Time Excellence: Productivity Strategies That Work',
        ],
        'organization_tips': [
            'Organization Mastery: Declutter and Optimize Your Life',
            'The Organization Blueprint: Create Order and Efficiency',
            'Organize Your Life: Systems for Success',
        ],
        'goal_setting': [
            'Goal Setting Mastery: Achieve Your Dreams Systematically',
            'The Goal Achievement Blueprint: Turn Dreams into Reality',
            'Goal Success: Strategies for Achievement',
        ],
        'workflow_optimization': [
            'Workflow Mastery: Optimize Processes for Maximum Efficiency',
            'The Workflow Blueprint: Streamline Your Productivity',
            'Process Excellence: Optimize Your Workflows',
        ],
        
        # Creative Writing & Storytelling
        'writing_techniques': [
            'Writing Mastery: Craft Compelling Stories and Content',
            'The Writing Blueprint: Master Writing Techniques',
            'Creative Writing Excellence: From Idea to Publication',
        ],
        'creative_prompts': [
            'Creative Writing Prompts: Spark Your Imagination',
            'The Creativity Blueprint: Unlock Your Writing Potential',
            'Writing Inspiration: Prompts for Creative Success',
        ],
        'genre_writing': [
            'Genre Writing Mastery: Excel in Your Chosen Style',
            'The Genre Blueprint: Master Specific Writing Styles',
            'Writing by Genre: Techniques for Success',
        ],
        'publishing_guide': [
            'Publishing Mastery: Get Your Work into the World',
            'The Publishing Blueprint: From Manuscript to Market',
            'Publishing Success: Your Guide to Getting Published',
        ],
        
        # Sustainability & Eco-Friendly Living
        'zero_waste': [
            'Zero Waste Mastery: Live Sustainably and Reduce Waste',
            'The Zero Waste Blueprint: Eco-Friendly Living Guide',
            'Waste-Free Living: Master Sustainable Habits',
        ],
        'renewable_energy': [
            'Renewable Energy Mastery: Power Your Home Sustainably',
            'The Energy Blueprint: Go Green with Renewable Power',
            'Clean Energy Success: Master Renewable Technologies',
        ],
        'sustainable_products': [
            'Sustainable Products Mastery: Choose Eco-Friendly Options',
            'The Sustainability Blueprint: Make Conscious Choices',
            'Green Living: Master Sustainable Product Selection',
        ],
        'eco_living': [
            'Eco-Friendly Living Mastery: Reduce Your Environmental Impact',
            'The Eco Blueprint: Live Sustainably Every Day',
            'Green Lifestyle Success: Master Eco-Friendly Living',
        ],
        
        # AI & Future Technologies
        'ai_concepts': [
            'AI Mastery: Understand Artificial Intelligence Fundamentals',
            'The AI Blueprint: Master Artificial Intelligence Concepts',
            'AI Understanding: From Basics to Advanced Concepts',
        ],
        'ai_ethics': [
            'AI Ethics Mastery: Navigate the Moral Landscape of Technology',
            'The Ethics Blueprint: Responsible AI Development',
            'Ethical AI: Master Technology Ethics and Governance',
        ],
        'future_tech_trends': [
            'Future Tech Mastery: Stay Ahead of Technology Trends',
            'The Future Blueprint: Master Emerging Technologies',
            'Tech Trends: Understanding Tomorrow\'s Innovations',
        ],
        'automation_impact': [
            'Automation Mastery: Understand Technology\'s Impact on Work',
            'The Automation Blueprint: Navigate the Future of Work',
            'Future Work: Master Automation and Technological Change',
        ],
        
        # Mindfulness & Meditation
        'mindfulness_practices': [
            'Mindfulness Mastery: Cultivate Present-Moment Awareness',
            'The Mindfulness Blueprint: Daily Practices for Inner Peace',
            'Present Moment Success: Master Mindfulness Techniques',
        ],
        'meditation_techniques': [
            'Meditation Mastery: Deepen Your Practice and Inner Peace',
            'The Meditation Blueprint: Techniques for Spiritual Growth',
            'Meditation Excellence: Master Various Meditation Styles',
        ],
        'stress_reduction': [
            'Stress Reduction Mastery: Find Calm in a Busy World',
            'The Calm Blueprint: Proven Stress Management Techniques',
            'Stress-Free Living: Master Relaxation and Peace',
        ],
        'inner_peace': [
            'Inner Peace Mastery: Find Tranquility and Spiritual Balance',
            'The Peace Blueprint: Journey to Inner Harmony',
            'Spiritual Wellness: Master Inner Peace Practices',
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
            # Handle both formats: "CHAPTER 1:" and "**CHAPTER 1:**"
            if line.startswith('CHAPTER ') or ('**CHAPTER ' in line and '**' in line):
                if current_chapter:
                    chapters.append(current_chapter)
                
                # Clean up the title
                title = line.replace('**', '').replace(':', '').strip()
                current_chapter = {
                    'title': title,
                    'content': []
                }
            elif current_chapter and line and not line.startswith('**') and not line.startswith('*'):
                # Skip markdown formatting lines, only add actual content
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
