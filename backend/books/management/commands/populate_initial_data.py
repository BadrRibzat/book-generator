from django.core.management.base import BaseCommand
from books.models import Domain, Niche, BookStyle, CoverStyle


class Command(BaseCommand):
    help = 'Populate initial data for domains, niches, book styles, and cover styles'

    def handle(self, *args, **options):
        self.stdout.write('Populating initial data...')

        # Create domains
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
                'name': 'Future Skills & Digital Economy',
                'slug': 'future_skills',
                'description': 'Future-ready skills and digital economy trends',
                'icon': 'fas fa-rocket',
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
                'name': 'Health & Wellness',
                'slug': 'health-wellness',
                'description': 'Fitness, nutrition, mental health, and lifestyle',
                'icon': 'fas fa-heartbeat',
                'order': 7
            },
            {
                'name': 'Personal Development',
                'slug': 'personal-development',
                'description': 'Self-improvement, motivation, and life skills',
                'icon': 'fas fa-user-graduate',
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

        # Create niches
        niches_data = [
            # AI & Digital Transformation
            {'domain': 'ai_digital_transformation', 'name': 'AI Business Automation', 'slug': 'ai_business_automation', 'audience': 'Business owners and managers', 'order': 1},
            {'domain': 'ai_digital_transformation', 'name': 'AI Ethics & Governance', 'slug': 'ai_ethics_governance', 'audience': 'Policy makers and executives', 'order': 2},
            {'domain': 'ai_digital_transformation', 'name': 'ChatGPT Productivity', 'slug': 'chatgpt_productivity', 'audience': 'Office workers and students', 'order': 3},
            {'domain': 'ai_digital_transformation', 'name': 'Machine Learning Basics', 'slug': 'machine_learning_basics', 'audience': 'Non-technical professionals', 'order': 4},

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

            # Future Skills
            {'domain': 'future_skills', 'name': 'Blockchain Fundamentals', 'slug': 'blockchain_fundamentals', 'audience': 'Finance and tech professionals', 'order': 1},
            {'domain': 'future_skills', 'name': 'Cybersecurity Essentials', 'slug': 'cybersecurity_essentials', 'audience': 'All internet users', 'order': 2},
            {'domain': 'future_skills', 'name': 'Metaverse Skills', 'slug': 'metaverse_skills', 'audience': 'Tech innovators', 'order': 3},
            {'domain': 'future_skills', 'name': 'Remote Work Mastery', 'slug': 'remote_work_mastery', 'audience': 'Remote workers', 'order': 4},

            # Health & Wellness
            {'domain': 'health-wellness', 'name': 'Fitness', 'slug': 'fitness', 'audience': 'Fitness enthusiasts', 'order': 1},
            {'domain': 'health-wellness', 'name': 'Nutrition', 'slug': 'nutrition', 'audience': 'Health-conscious individuals', 'order': 2},
            {'domain': 'health-wellness', 'name': 'Mental Health', 'slug': 'mental_health', 'audience': 'General public', 'order': 3},
            {'domain': 'health-wellness', 'name': 'Weight Loss', 'slug': 'weight_loss', 'audience': 'Weight loss seekers', 'order': 4},

            # Mental Health Tech
            {'domain': 'mental_health_tech', 'name': 'AI Mental Health Apps', 'slug': 'ai_mental_health_apps', 'audience': 'Healthcare providers', 'order': 1},
            {'domain': 'mental_health_tech', 'name': 'Digital Wellness Tools', 'slug': 'digital_wellness_tools', 'audience': 'Wellness seekers', 'order': 2},
            {'domain': 'mental_health_tech', 'name': 'Mental Health Wearables', 'slug': 'mental_health_wearables', 'audience': 'Health-conscious individuals', 'order': 3},
            {'domain': 'mental_health_tech', 'name': 'Teletherapy Platforms', 'slug': 'teletherapy_platforms', 'audience': 'Therapists and patients', 'order': 4},

            # Personal Development
            {'domain': 'personal-development', 'name': 'Productivity', 'slug': 'productivity', 'audience': 'Professionals and students', 'order': 1},
            {'domain': 'personal-development', 'name': 'Motivation', 'slug': 'motivation', 'audience': 'General public', 'order': 2},
            {'domain': 'personal-development', 'name': 'Communication', 'slug': 'communication', 'audience': 'Professionals', 'order': 3},
            {'domain': 'personal-development', 'name': 'Mindfulness', 'slug': 'mindfulness', 'audience': 'Stress management seekers', 'order': 4},

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

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data!'))