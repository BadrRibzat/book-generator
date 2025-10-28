from django.core.management.base import BaseCommand
from django.utils.text import slugify
from books.models import Domain, Niche


class Command(BaseCommand):
    help = "Seed additional niches to reach >=200 across active domains"

    def add_arguments(self, parser):
        parser.add_argument('--per-domain', type=int, default=25, help='Target niches per domain (approximate)')
        parser.add_argument('--force', action='store_true', help='Create even if already >= target')

    def handle(self, *args, **options):
        per_domain = options['per_domain']
        force = options['force']

        self.stdout.write(f"Seeding additional niches (target ~{per_domain} per domain)...")

        # Domain-specific topic seeds
        seeds = {
            'ai_digital_transformation': [
                'AI Strategy', 'Automation Playbooks', 'Prompt Engineering', 'Data Governance', 'Responsible AI',
                'AI in Marketing', 'AI in HR', 'AI in Finance', 'AI in Operations', 'Citizen Development',
                'GenAI Adoption', 'AI Project Management', 'RAG Systems', 'LLM Safety', 'Edge AI',
            ],
            'ai_automation': [
                'No-Code Automation', 'Workflow Design', 'Zapier Blueprints', 'Make.com Systems', 'SaaS Automation',
                'CRM Automation', 'Email Automation', 'Sales Playbooks', 'Support Automation', 'Back-office RPA',
                'Automation Metrics', 'Team Onboarding', 'Quality Gates', 'Scaling Automation', 'AI Agents',
            ],
            'ecommerce_digital_products': [
                'Shopify Growth', 'Amazon Listings', 'POD Niches', 'Email Funnels', 'SEO for Stores',
                'Facebook Ads', 'TikTok Ads', 'UGC for Ecommerce', 'Conversion Rate Optimization', 'A/B Testing',
                'Bundles & Upsells', 'Customer Retention', 'Subscriptions', 'Influencer Collabs', 'Logistics Basics',
            ],
            'parenting_preschool_learning': [
                'Speech Sounds', 'Phonological Awareness', 'Play-Based Learning', 'Fine Motor Skills', 'Sensory Play',
                'Story Time Routines', 'Vocabulary Games', 'Bilingual Basics', 'Social Skills', 'Daily Routines',
                'Screen Time Balance', 'Calm Down Tools', 'Positive Reinforcement', 'Outdoor Learning', 'Numbers & Counting',
            ],
            'sustainability_green_tech': [
                'Home Solar', 'Heat Pumps', 'EV Ownership', 'Zero Waste', 'Composting',
                'Water Conservation', 'Green Investing', 'Eco-Friendly Products', 'Circular Design', 'Carbon Tracking',
                'Sustainable Fashion', 'Green Supply Chains', 'Community Gardens', 'Urban Farming', 'Eco Habits',
            ],
            'mental_health_tech': [
                'Mindfulness Apps', 'CBT Tools', 'Teletherapy Tips', 'Sleep Hygiene', 'Stress Tracking',
                'Digital Detox', 'Wearables', 'Anxiety Supports', 'ADHD Routines', 'Journaling Systems',
                'Habit Building', 'Resilience Skills', 'Breathing Exercises', 'Caregiver Guides', 'Youth Wellbeing',
            ],
            'technology': [
                'Web Dev Foundations', 'APIs & Integrations', 'Cloud Basics', 'Data Analysis', 'Python for Everyone',
                'Frontend Skills', 'Backend Patterns', 'DevOps Intro', 'Testing & QA', 'Security Essentials',
                'Open Source', 'Design Systems', 'UX Writing', 'Accessibility', 'AI for Developers',
            ],
            'business': [
                'Lean Startup', 'Personal Branding', 'Solopreneur Systems', 'Pricing Strategy', 'Go-To-Market',
                'Sales Playbooks', 'Negotiation', 'Business Models', 'OKRs & KPIs', 'Storytelling',
                'Team Culture', 'Remote Work', 'Finance 101', 'Fundraising', 'Customer Discovery',
            ],
            'education': [
                'Study Habits', 'Note-Taking', 'Memory Techniques', 'Active Recall', 'Spaced Repetition',
                'Online Learning', 'Project-Based Learning', 'Peer Teaching', 'Assessment Design', 'EdTech Tools',
                'Critical Thinking', 'Reading Strategies', 'Essay Writing', 'STEM Activities', 'Language Learning',
            ],
            'creative-arts': [
                'Creative Writing', 'Story Structure', 'Graphic Design', 'Typography Basics', 'Color Theory',
                'Photography Basics', 'Composition', 'Music Production', 'Songwriting', 'Illustration',
                'Brand Design', 'Portfolio Craft', 'Digital Painting', 'Animation Intro', 'Content Strategy',
            ],
        }

        modifiers = [
            'Fundamentals', 'Beginner Guide', 'Advanced Techniques', '2025 Strategies', 'Playbook',
            'Templates & Checklists', 'Case Studies', 'Step-by-Step', 'Frameworks', 'Action Plan'
        ]

        total_created = 0
        for domain in Domain.objects.filter(is_active=True).order_by('order'):
            desired = per_domain
            existing = Niche.objects.filter(domain=domain, is_active=True).count()
            if existing >= desired and not force:
                self.stdout.write(f"Domain {domain.slug}: already has {existing} niches (>= target), skipping")
                continue

            to_create = max(0, desired - existing)
            base_topics = seeds.get(domain.slug, seeds.get(domain.slug.replace('-', '_'), []))
            if not base_topics:
                # Fallback generic topics
                base_topics = [f"Essentials {i}" for i in range(1, 16)]

            created_here = 0
            i = 0
            while created_here < to_create and i < 1000:
                i += 1
                topic = base_topics[i % len(base_topics)]
                mod = modifiers[i % len(modifiers)]
                name = f"{topic}: {mod}"
                slug = slugify(name)[:90]
                # Ensure uniqueness within domain
                if Niche.objects.filter(domain=domain, slug=slug).exists():
                    slug = f"{slug}-{i}"
                try:
                    Niche.objects.create(
                        domain=domain,
                        name=name,
                        slug=slug,
                        description=f"{name} for {domain.name.lower()}.",
                        audience="Professionals and learners",
                        market_size="Growing",
                        order=existing + created_here + 1,
                        is_active=True,
                    )
                    created_here += 1
                except Exception:
                    continue

            total_created += created_here
            self.stdout.write(f"Domain {domain.slug}: created {created_here} new niches (now ~{existing + created_here})")

        self.stdout.write(self.style.SUCCESS(f"Done. Created {total_created} additional niches."))
