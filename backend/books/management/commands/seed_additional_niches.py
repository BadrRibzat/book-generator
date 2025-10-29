from django.core.management.base import BaseCommand
from django.utils.text import slugify
from books.models import Domain, Niche
from books.data.guided_catalog import GUIDED_CATALOG


class Command(BaseCommand):
    help = "Seed additional niches to reach >=200 across active domains"

    def add_arguments(self, parser):
        parser.add_argument('--per-domain', type=int, default=25, help='Target niches per domain (approximate)')
        parser.add_argument('--force', action='store_true', help='Create even if already >= target')

    def handle(self, *args, **options):
        per_domain = options['per_domain']
        force = options['force']

        self.stdout.write(f"Seeding additional niches (target ~{per_domain} per domain)...")

        catalog_map = {domain['slug']: domain for domain in GUIDED_CATALOG}

        seed_overrides = {
            'artificial_intelligence_machine_learning': [
                'AI Operating Models', 'Responsible AI Governance', 'Retrieval-Augmented Generation', 'Edge AI Systems', 'AI Product Management',
            ],
            'health_wellness_technology': [
                'Digital Care Pathways', 'Behavioral Health Journeys', 'Virtual Coaching Models', 'Clinical Data Interoperability', 'Remote Patient Monitoring',
            ],
            'sustainable_tech_green_energy': [
                'Net-Zero Roadmaps', 'ESG Reporting Playbooks', 'Carbon Market Strategies', 'Sustainable Supply Chains', 'Green Financing Programs',
            ],
            'remote_work_digital_collaboration': [
                'Async Decision Frameworks', 'Distributed Leadership', 'Virtual Onboarding Systems', 'Team Ritual Design', 'Collaboration Analytics',
            ],
            'cybersecurity': [
                'Security Automation', 'Threat Hunting Guides', 'Incident Response Sprints', 'Governance Risk & Compliance', 'Security Metrics Dashboards',
            ],
            'creator_economy_digital_content': [
                'Community Monetization', 'Cross-Platform Distribution', 'Creator Analytics', 'Collaborative Studios', 'Brand Partnership Playbooks',
            ],
            'web3_blockchain': [
                'Tokenomics Design', 'Compliance in Web3', 'Onboarding Web2 Users', 'DAO Operations', 'Cross-Chain Strategies',
            ],
            'edtech_online_learning': [
                'Learning Experience Design', 'Instructor Enablement', 'Assessment Innovation', 'Learning Analytics', 'Community-Driven Cohorts',
            ],
            'ecommerce_retail_tech': [
                'Marketplace Expansion', 'Retail Media Networks', 'Post-Purchase Journeys', 'Customer Lifetime Value Playbooks', 'Logistics Automation',
            ],
            'fintech': [
                'Risk & Compliance Automation', 'Financial Data Platforms', 'Capital Formation Tools', 'Treasury Automation', 'Fraud Prevention Systems',
            ],
            'data_analytics_business_intelligence': [
                'Analytics Centers of Excellence', 'Self-Service BI Enablement', 'Data Product Management', 'Decision Intelligence', 'Data Governance Frameworks',
            ],
            'gaming_interactive_entertainment': [
                'Creator UGC Systems', 'Live Ops Playbooks', 'Player Retention Science', 'Monetization Analytics', 'Community Expansion',
            ],
            'automation': [
                'Automation Program Management', 'Process Discovery Workshops', 'Citizen Developer Enablement', 'Automation Center of Excellence', 'AI Agent Handoffs',
            ],
        }

        modifiers = [
            'Playbook', 'Blueprint', 'Field Manual', 'Sprint Plan', 'Toolkit',
            'Workshop Series', 'Action Plan', 'Case Studies', 'Frameworks', 'Quickstart'
        ]

        total_created = 0
        for domain in Domain.objects.filter(is_active=True).order_by('order'):
            desired = per_domain
            existing = Niche.objects.filter(domain=domain, is_active=True).count()
            if existing >= desired and not force:
                self.stdout.write(f"Domain {domain.slug}: already has {existing} niches (>= target), skipping")
                continue

            to_create = max(0, desired - existing)
            domain_payload = catalog_map.get(domain.slug)
            base_topics = []
            if domain_payload:
                base_topics.extend(n['name'] for n in domain_payload['niches'])
            base_topics.extend(seed_overrides.get(domain.slug, []))
            base_topics = base_topics or [f"Essentials {i}" for i in range(1, 16)]

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
                        prompt_template=(
                            f"You are creating a concise guide on {name.lower()} for the {domain.name} domain."
                            " Provide practical steps, curated tools, and measurable checkpoints."
                        ),
                        content_skeleton=[
                            {'title': 'Goals & Success Metrics', 'summary': 'Define what success looks like and how to measure it.'},
                            {'title': 'Core Framework', 'summary': 'Lay out the key pillars or steps for the topic.'},
                            {'title': 'Execution Roadmap', 'summary': 'Walk through actionable weekly sprints.'},
                            {'title': 'Tools & Templates', 'summary': 'Recommend essential resources and templates.'},
                            {'title': 'Case Spotlight', 'summary': 'Share an illustrative example or case study.'},
                            {'title': 'Next Steps', 'summary': 'Outline follow-up actions and learning paths.'},
                        ],
                        order=existing + created_here + 1,
                        is_active=True,
                    )
                    created_here += 1
                except Exception:
                    continue

            total_created += created_here
            self.stdout.write(f"Domain {domain.slug}: created {created_here} new niches (now ~{existing + created_here})")

        self.stdout.write(self.style.SUCCESS(f"Done. Created {total_created} additional niches."))
