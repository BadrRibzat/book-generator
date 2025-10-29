from django.core.management.base import BaseCommand
from books.models import Domain, Niche, CoverStyle, FontTheme, Book, BookTemplate
from books.data.guided_catalog import GUIDED_CATALOG, DOMAIN_SLUGS


class Command(BaseCommand):
    help = 'Populate initial data for domains, niches, book styles, cover styles, and font themes'

    def handle(self, *args, **options):
        self.stdout.write('Populating initial data...')

        desired_order = DOMAIN_SLUGS

        legacy_domains = Domain.objects.exclude(slug__in=desired_order)
        if legacy_domains.exists():
            Book.objects.filter(domain__in=legacy_domains).delete()
            BookTemplate.objects.filter(domain__in=legacy_domains).delete()
            legacy_domains.delete()

        domains = {}
        for idx, domain_payload in enumerate(GUIDED_CATALOG, start=1):
            domain, created = Domain.objects.update_or_create(
                slug=domain_payload['slug'],
                defaults={
                    'name': domain_payload['name'],
                    'description': domain_payload['description'],
                    'icon': domain_payload['icon'],
                    'order': idx,
                    'is_active': True,
                }
            )
            domains[domain_payload['slug']] = domain
            action = 'Created' if created else 'Updated'
            self.stdout.write(f"{action} domain: {domain.name}")

            desired_niche_slugs = [n['slug'] for n in domain_payload['niches']]
            removable_niches = domain.niches.exclude(slug__in=desired_niche_slugs)
            if removable_niches.exists():
                Book.objects.filter(niche__in=removable_niches).delete()
                BookTemplate.objects.filter(niche__in=removable_niches).delete()
                removable_niches.delete()

            for order, niche in enumerate(domain_payload['niches'], start=1):
                defaults = {
                    'name': niche['name'],
                    'description': niche['description'],
                    'prompt_template': niche['prompt_template'],
                    'content_skeleton': niche['content_skeleton'],
                    'order': order,
                    'is_active': niche.get('is_active', True),
                }
                niche_obj, created = Niche.objects.update_or_create(
                    domain=domain,
                    slug=niche['slug'],
                    defaults=defaults
                )
                action = 'Created' if created else 'Updated'
                self.stdout.write(f"  {action} niche: {niche_obj.name}")
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
            {
                'name': 'Professional Default',
                'category': 'clean_sans',
                'description': 'Clean modern fonts for professional content',
                'domain_slug': None,
                'header_font': 'Inter',
                'body_font': 'Lato',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['professional', 'clean', 'modern', 'minimal', 'corporate'],
                'priority': 100,
                'is_default': True
            },
            {
                'name': 'Automation Clean',
                'category': 'clean_sans',
                'description': 'Clean fonts for automation content',
                'domain_slug': 'automation',
                'header_font': 'Work Sans',
                'body_font': 'Source Sans Pro',
                'header_weight': 600,
                'body_weight': 400,
                'ai_brief_keywords': ['automation', 'workflow', 'system', 'process'],
                'priority': 90
            },
            {
                'name': 'Healthy Rounded',
                'category': 'hand_written',
                'description': 'Friendly fonts for wellness and lifestyle content',
                'domain_slug': 'health_wellness_technology',
                'header_font': 'Quicksand',
                'body_font': 'Nunito',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['health', 'wellness', 'family', 'friendly', 'supportive', 'care'],
                'priority': 90
            },
            {
                'name': 'E-commerce Bold',
                'category': 'clean_sans',
                'description': 'Bold readable fonts for e-commerce',
                'domain_slug': 'ecommerce_retail_tech',
                'header_font': 'Montserrat',
                'body_font': 'Lato',
                'header_weight': 800,
                'body_weight': 400,
                'ai_brief_keywords': ['commerce', 'business', 'selling', 'marketing', 'bold'],
                'priority': 85
            },
            {
                'name': 'Data-Driven Minimal',
                'category': 'clean_sans',
                'description': 'Minimalist fonts for analytics and strategy content',
                'domain_slug': 'data_analytics_business_intelligence',
                'header_font': 'IBM Plex Sans',
                'body_font': 'Source Sans Pro',
                'header_weight': 600,
                'body_weight': 400,
                'ai_brief_keywords': ['analytics', 'insights', 'dashboard', 'data', 'strategy'],
                'priority': 80
            },
            {
                'name': 'Elegant Serif',
                'category': 'elegant_serif',
                'description': 'Classic elegant serif fonts',
                'domain_slug': None,
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
                'domain_slug': None,
                'header_font': 'Dancing Script',
                'body_font': 'Cabin',
                'header_weight': 700,
                'body_weight': 400,
                'ai_brief_keywords': ['personal', 'casual', 'handwritten', 'informal', 'friendly'],
                'priority': 60
            },
        ]

        for font_data in font_themes_data:
            domain_slug = font_data.pop('domain_slug')
            domain_obj = domains.get(domain_slug) if domain_slug else None
            defaults = {**font_data, 'domain': domain_obj}
            font_theme, created = FontTheme.objects.update_or_create(
                name=font_data['name'],
                defaults=defaults
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} font theme: {font_theme.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data!'))