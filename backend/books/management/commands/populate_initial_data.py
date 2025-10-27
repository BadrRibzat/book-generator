from django.core.management.base import BaseCommand
from books.models import Domain, Niche, BookStyle, CoverStyle, FontTheme


class Command(BaseCommand):
    help = 'Populate initial data for domains, niches, book styles, cover styles, and font themes'

    def handle(self, *args, **options):
        self.stdout.write('Populating initial data...')

        # Create domains - with new trending domains
        domains_data = [
            {
                'name': 'AI & Digital Transformation',
                'slug': 'ai_digital_transformation',
                'description': 'AI, automation, and digital business transformation',
                'icon': 'fas fa-robot',
                'order': 1
            },
            {
                'name': 'Sustainability & Green Tech',
                'slug': 'sustainability_green_tech',
                'description': 'Green technology and sustainable business practices',
                'icon': 'fas fa-leaf',
                'order': 2
            },
            {
                'name': 'Mental Health Technology',
                'slug': 'mental_health_tech',
                'description': 'Technology solutions for mental health and wellness',
                'icon': 'fas fa-brain',
                'order': 3
            },
            {
                'name': 'E-commerce & Digital Products',  # NEW - Replaces old domain
                'slug': 'ecommerce_digital_products',
                'description': 'Online business, digital products, and e-commerce strategies',
                'icon': 'fas fa-shopping-cart',
                'order': 4
            },
            {
                'name': 'Technology',
                'slug': 'technology',
                'description': 'Books about software, hardware, AI, and digital innovation',
                'icon': 'fas fa-laptop-code',
                'order': 5
            },
            {
                'name': 'Business',
                'slug': 'business',
                'description': 'Entrepreneurship, management, marketing, and finance',
                'icon': 'fas fa-briefcase',
                'order': 6
            },
            {
                'name': 'Parenting: Pre-school Speech & Learning',  # NEW - Replaces old domain
                'slug': 'parenting_preschool_learning',
                'description': 'Early childhood development, speech therapy, and preschool learning',
                'icon': 'fas fa-child',
                'order': 7
            },
            {
                'name': 'AI & Automation',  # NEW - Replaces old domain
                'slug': 'ai_automation',
                'description': 'AI tools, automation strategies, and intelligent systems',
                'icon': 'fas fa-cogs',
                'order': 8
            },
            {
                'name': 'Education',
                'slug': 'education',
                'description': 'Learning methods, study skills, and academic success',
                'icon': 'fas fa-graduation-cap',
                'order': 9
            },
            {
                'name': 'Creative Arts',
                'slug': 'creative-arts',
                'description': 'Writing, design, music, and artistic expression',
                'icon': 'fas fa-palette',
                'order': 10
            }
        ]

        domains = {}
        for domain_data in domains_data:
            domain, created = Domain.objects.get_or_create(
                slug=domain_data['slug'],
                defaults=domain_data
            )
            domains[domain_data['slug']] = domain
            if created:
                self.stdout.write(f'Created domain: {domain.name}')

        # Create niches with micro-workflows for new domains
        niches_data = [
            # AI & Digital Transformation
            {'domain': 'ai_digital_transformation', 'name': 'AI Business Automation', 'slug': 'ai_business_automation', 'audience': 'Business owners and managers', 'order': 1},
            {'domain': 'ai_digital_transformation', 'name': 'AI Ethics & Governance', 'slug': 'ai_ethics_governance', 'audience': 'Policy makers and executives', 'order': 2},
            {'domain': 'ai_digital_transformation', 'name': 'ChatGPT Productivity', 'slug': 'chatgpt_productivity', 'audience': 'Office workers and students', 'order': 3},
            {'domain': 'ai_digital_transformation', 'name': 'Machine Learning Basics', 'slug': 'machine_learning_basics', 'audience': 'Non-technical professionals', 'order': 4},

            # E-commerce & Digital Products (NEW - 5 micro-workflows)
            {'domain': 'ecommerce_digital_products', 'name': 'Dropshipping Mastery', 'slug': 'dropshipping_mastery', 'audience': 'Aspiring e-commerce entrepreneurs', 'order': 1},
            {'domain': 'ecommerce_digital_products', 'name': 'Digital Product Creation', 'slug': 'digital_product_creation', 'audience': 'Content creators and course makers', 'order': 2},
            {'domain': 'ecommerce_digital_products', 'name': 'Amazon FBA Success', 'slug': 'amazon_fba_success', 'audience': 'Online sellers', 'order': 3},
            {'domain': 'ecommerce_digital_products', 'name': 'Shopify Store Building', 'slug': 'shopify_store_building', 'audience': 'E-commerce store owners', 'order': 4},
            {'domain': 'ecommerce_digital_products', 'name': 'Print on Demand Business', 'slug': 'print_on_demand', 'audience': 'Creative entrepreneurs', 'order': 5},

            # Parenting: Pre-school Speech & Learning (NEW - 5 micro-workflows)
            {'domain': 'parenting_preschool_learning', 'name': 'Speech Development 3-6 Years', 'slug': 'speech_development_3_6', 'audience': 'Parents and caregivers', 'order': 1},
            {'domain': 'parenting_preschool_learning', 'name': 'Phonics & Early Reading', 'slug': 'phonics_early_reading', 'audience': 'Parents and educators', 'order': 2},
            {'domain': 'parenting_preschool_learning', 'name': 'Preschool Learning Activities', 'slug': 'preschool_activities', 'audience': 'Parents and early educators', 'order': 3},
            {'domain': 'parenting_preschool_learning', 'name': 'Language Delay Support', 'slug': 'language_delay_support', 'audience': 'Parents with speech-delayed children', 'order': 4},
            {'domain': 'parenting_preschool_learning', 'name': 'Bilingual Preschool Learning', 'slug': 'bilingual_preschool', 'audience': 'Multilingual families', 'order': 5},

            # AI & Automation (NEW - 5 micro-workflows)
            {'domain': 'ai_automation', 'name': 'No-Code AI Tools', 'slug': 'no_code_ai_tools', 'audience': 'Non-technical professionals', 'order': 1},
            {'domain': 'ai_automation', 'name': 'Marketing Automation', 'slug': 'marketing_automation', 'audience': 'Digital marketers', 'order': 2},
            {'domain': 'ai_automation', 'name': 'Workflow Automation', 'slug': 'workflow_automation', 'audience': 'Operations managers', 'order': 3},
            {'domain': 'ai_automation', 'name': 'AI Content Creation', 'slug': 'ai_content_creation', 'audience': 'Content creators', 'order': 4},
            {'domain': 'ai_automation', 'name': 'RPA for Business', 'slug': 'rpa_business', 'audience': 'Business process managers', 'order': 5},

            # Business
            {'domain': 'business', 'name': 'Entrepreneurship', 'slug': 'entrepreneurship', 'audience': 'Aspiring entrepreneurs', 'order': 1},
            {'domain': 'business', 'name': 'Digital Marketing', 'slug': 'digital_marketing', 'audience': 'Marketers and business owners', 'order': 2},
            {'domain': 'business', 'name': 'E-commerce', 'slug': 'ecommerce', 'audience': 'Online sellers', 'order': 3},
            {'domain': 'business', 'name': 'Leadership', 'slug': 'leadership', 'audience': 'Managers and executives', 'order': 4},

            # Creative Arts
            {'domain': 'creative-arts', 'name': 'Writing', 'slug': 'writing', 'audience': 'Writers and authors', 'order': 1},
            {'domain': 'creative-arts', 'name': 'Graphic Design', 'slug': 'graphic_design', 'audience': 'Designers and creatives', 'order': 2},
            {'domain': 'creative-arts', 'name': 'Photography', 'slug': 'photography', 'audience': 'Photography enthusiasts', 'order': 3},
            {'domain': 'creative-arts', 'name': 'Music Production', 'slug': 'music_production', 'audience': 'Musicians and producers', 'order': 4},

            # Education
            {'domain': 'education', 'name': 'Study Skills', 'slug': 'study_skills', 'audience': 'Students', 'order': 1},
            {'domain': 'education', 'name': 'Online Learning', 'slug': 'online_learning', 'audience': 'Educators and learners', 'order': 2},
            {'domain': 'education', 'name': 'Language Learning', 'slug': 'language_learning', 'audience': 'Language learners', 'order': 3},
            {'domain': 'education', 'name': 'Test Prep', 'slug': 'test_prep', 'audience': 'Students', 'order': 4},

            # Mental Health Tech
            {'domain': 'mental_health_tech', 'name': 'AI Mental Health Apps', 'slug': 'ai_mental_health_apps', 'audience': 'Healthcare providers', 'order': 1},
            {'domain': 'mental_health_tech', 'name': 'Digital Wellness Tools', 'slug': 'digital_wellness_tools', 'audience': 'Wellness seekers', 'order': 2},
            {'domain': 'mental_health_tech', 'name': 'Mental Health Wearables', 'slug': 'mental_health_wearables', 'audience': 'Health-conscious individuals', 'order': 3},
            {'domain': 'mental_health_tech', 'name': 'Teletherapy Platforms', 'slug': 'teletherapy_platforms', 'audience': 'Therapists and patients', 'order': 4},

            # Sustainability
            {'domain': 'sustainability_green_tech', 'name': 'Carbon Neutral Living', 'slug': 'carbon_neutral_living', 'audience': 'Environmentally conscious consumers', 'order': 1},
            {'domain': 'sustainability_green_tech', 'name': 'Circular Economy Principles', 'slug': 'circular_economy_principles', 'audience': 'Business leaders', 'order': 2},
            {'domain': 'sustainability_green_tech', 'name': 'Green Technology Innovations', 'slug': 'green_technology_innovations', 'audience': 'Tech enthusiasts', 'order': 3},
            {'domain': 'sustainability_green_tech', 'name': 'Renewable Energy Solutions', 'slug': 'renewable_energy_solutions', 'audience': 'Homeowners and businesses', 'order': 4},

            # Technology
            {'domain': 'technology', 'name': 'Artificial Intelligence', 'slug': 'artificial_intelligence', 'audience': 'Tech professionals and enthusiasts', 'order': 1},
            {'domain': 'technology', 'name': 'Web Development', 'slug': 'web_development', 'audience': 'Developers and startups', 'order': 2},
            {'domain': 'technology', 'name': 'Mobile Apps', 'slug': 'mobile_apps', 'audience': 'App developers and entrepreneurs', 'order': 3},
            {'domain': 'technology', 'name': 'Data Science', 'slug': 'data_science', 'audience': 'Data professionals', 'order': 4},
        ]

        for niche_data in niches_data:
            domain_slug = niche_data.pop('domain')  # Remove domain from niche_data
            domain = domains.get(domain_slug)
            if domain:
                niche_data['domain'] = domain  # Add domain instance
                niche, created = Niche.objects.get_or_create(
                    domain=domain,
                    slug=niche_data['slug'],
                    defaults=niche_data
                )
                if created:
                    self.stdout.write(f'Created niche: {niche.name}')

        # Create book styles
        book_styles_data = [
            {'name': 'Educational Professional', 'tone': 'educational', 'target_audience': 'professionals', 'language': 'en', 'length': 'medium', 'description': 'Educational content for professionals', 'order': 1},
            {'name': 'Inspirational General', 'tone': 'inspirational', 'target_audience': 'general', 'language': 'en', 'length': 'medium', 'description': 'Inspirational content for general audience', 'order': 2},
            {'name': 'Technical Students', 'tone': 'technical', 'target_audience': 'students', 'language': 'en', 'length': 'medium', 'description': 'Technical content for students', 'order': 3},
            {'name': 'Conversational Parents', 'tone': 'conversational', 'target_audience': 'parents', 'language': 'en', 'length': 'medium', 'description': 'Conversational content for parents', 'order': 4},
            {'name': 'Professional Entrepreneurs', 'tone': 'professional', 'target_audience': 'entrepreneurs', 'language': 'en', 'length': 'medium', 'description': 'Professional content for entrepreneurs', 'order': 5},
            {'name': 'Playful Kids', 'tone': 'playful', 'target_audience': 'kids', 'language': 'en', 'length': 'short', 'description': 'Playful content for kids', 'order': 6},
            {'name': 'Educational Students', 'tone': 'educational', 'target_audience': 'students', 'language': 'en', 'length': 'medium', 'description': 'Educational content for students', 'order': 7},
        ]

        for style_data in book_styles_data:
            style, created = BookStyle.objects.get_or_create(
                name=style_data['name'],
                defaults=style_data
            )
            if created:
                self.stdout.write(f'Created book style: {style.name}')

        # Create cover styles
        cover_styles_data = [
            {'name': 'Minimalist Clean', 'style': 'minimalist', 'description': 'Clean, simple design with plenty of white space', 'color_scheme': {'primary': '#FFFFFF', 'accent': '#000000'}, 'order': 1},
            {'name': 'Futuristic Tech', 'style': 'futuristic', 'description': 'Modern tech-inspired design with gradients', 'color_scheme': {'primary': '#1a1a2e', 'accent': '#00d4ff'}, 'order': 2},
            {'name': 'Playful Colorful', 'style': 'playful', 'description': 'Bright, colorful design for fun topics', 'color_scheme': {'primary': '#ff6b6b', 'accent': '#4ecdc4'}, 'order': 3},
            {'name': 'Elegant Professional', 'style': 'elegant', 'description': 'Sophisticated design for business topics', 'color_scheme': {'primary': '#2c3e50', 'accent': '#e74c3c'}, 'order': 4},
            {'name': 'Corporate Blue', 'style': 'corporate', 'description': 'Professional blue theme for corporate content', 'color_scheme': {'primary': '#3498db', 'accent': '#2c3e50'}, 'order': 5},
            {'name': 'Artistic Creative', 'style': 'artistic', 'description': 'Creative, artistic design with unique elements', 'color_scheme': {'primary': '#9b59b6', 'accent': '#f1c40f'}, 'order': 6},
        ]

        for cover_data in cover_styles_data:
            cover, created = CoverStyle.objects.get_or_create(
                name=cover_data['name'],
                defaults=cover_data
            )
            if created:
                self.stdout.write(f'Created cover style: {cover.name}')

        # Create font themes with domain-specific and AI brief keywords
        font_themes_data = [
            # Default professional theme
            {
                'name': 'Professional Default',
                'category': 'clean_sans',
                'description': 'Clean modern fonts for professional content',
                'domain': None,
                'header_font': 'Inter',
                'body_font': 'Lato',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['professional', 'clean', 'modern', 'minimal', 'corporate'],
                'priority': 100,
                'is_default': True
            },
            # Tech/AI domains
            {
                'name': 'Tech Modern',
                'category': 'modern_geometric',
                'description': 'Modern geometric fonts for tech content',
                'domain': domains.get('ai_digital_transformation'),
                'header_font': 'Roboto',
                'body_font': 'Open Sans',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['tech', 'digital', 'ai', 'futuristic', 'modern', 'innovation'],
                'priority': 90
            },
            {
                'name': 'Automation Clean',
                'category': 'clean_sans',
                'description': 'Clean fonts for automation content',
                'domain': domains.get('ai_automation'),
                'header_font': 'Work Sans',
                'body_font': 'Source Sans Pro',
                'header_weight': 600,
                'body_weight': 400,
                'ai_brief_keywords': ['automation', 'workflow', 'system', 'process'],
                'priority': 85
            },
            # E-commerce
            {
                'name': 'E-commerce Bold',
                'category': 'clean_sans',
                'description': 'Bold readable fonts for e-commerce',
                'domain': domains.get('ecommerce_digital_products'),
                'header_font': 'Montserrat',
                'body_font': 'Lato',
                'header_weight': 800,
                'body_weight': 400,
                'ai_brief_keywords': ['commerce', 'business', 'selling', 'marketing', 'bold'],
                'priority': 85
            },
            # Parenting/Kids
            {
                'name': 'Friendly Rounded',
                'category': 'hand_written',
                'description': 'Friendly fonts for parenting and kids content',
                'domain': domains.get('parenting_preschool_learning'),
                'header_font': 'Quicksand',
                'body_font': 'Nunito',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['playful', 'kids', 'family', 'friendly', 'warm', 'children', 'preschool'],
                'priority': 90
            },
            # Sustainability
            {
                'name': 'Eco Natural',
                'category': 'elegant_serif',
                'description': 'Natural elegant fonts for sustainability',
                'domain': domains.get('sustainability_green_tech'),
                'header_font': 'Merriweather',
                'body_font': 'Lora',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['eco', 'natural', 'sustainable', 'green', 'organic', 'earth'],
                'priority': 85
            },
            # Mental Health
            {
                'name': 'Calm Serene',
                'category': 'elegant_serif',
                'description': 'Calm serif fonts for wellness content',
                'domain': domains.get('mental_health_tech'),
                'header_font': 'Crimson Text',
                'body_font': 'Source Serif Pro',
                'header_weight': 600,
                'body_weight': 400,
                'ai_brief_keywords': ['calm', 'wellness', 'mental', 'mindful', 'serene', 'peaceful'],
                'priority': 85
            },
            # Creative Arts
            {
                'name': 'Creative Artistic',
                'category': 'hand_written',
                'description': 'Artistic fonts for creative content',
                'domain': domains.get('creative-arts'),
                'header_font': 'Playfair Display',
                'body_font': 'Raleway',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['creative', 'artistic', 'design', 'elegant', 'stylish'],
                'priority': 85
            },
            # Global fallback themes
            {
                'name': 'Elegant Serif',
                'category': 'elegant_serif',
                'description': 'Classic elegant serif fonts',
                'domain': None,
                'header_font': 'Playfair Display',
                'body_font': 'Source Serif Pro',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['elegant', 'sophisticated', 'classic', 'traditional', 'formal'],
                'priority': 70
            },
            {
                'name': 'Hand-Written Style',
                'category': 'hand_written',
                'description': 'Hand-written style fonts for personal touch',
                'domain': None,
                'header_font': 'Dancing Script',
                'body_font': 'Cabin',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['personal', 'casual', 'handwritten', 'informal', 'friendly'],
                'priority': 60
            },
        ]

        for font_data in font_themes_data:
            # Handle domain None case
            domain_obj = font_data.pop('domain')
            font_theme, created = FontTheme.objects.get_or_create(
                name=font_data['name'],
                defaults={**font_data, 'domain': domain_obj}
            )
            if created:
                self.stdout.write(f'Created font theme: {font_theme.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data!'))