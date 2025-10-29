from django.db import migrations


def apply_guided_catalog(apps, schema_editor):
    from books.data.guided_catalog import GUIDED_CATALOG, DOMAIN_SLUGS

    Domain = apps.get_model('books', 'Domain')
    Niche = apps.get_model('books', 'Niche')
    Book = apps.get_model('books', 'Book')
    BookTemplate = apps.get_model('books', 'BookTemplate')

    legacy_domains = Domain.objects.exclude(slug__in=DOMAIN_SLUGS)
    if legacy_domains.exists():
        Book.objects.filter(domain__in=legacy_domains).delete()
        BookTemplate.objects.filter(domain__in=legacy_domains).delete()
        legacy_domains.delete()

    for order, domain_payload in enumerate(GUIDED_CATALOG, start=1):
        domain, _ = Domain.objects.update_or_create(
            slug=domain_payload['slug'],
            defaults={
                'name': domain_payload['name'],
                'description': domain_payload['description'],
                'icon': domain_payload['icon'],
                'order': order,
                'is_active': True,
            }
        )

        allowed_niche_slugs = [n['slug'] for n in domain_payload['niches']]
        removable_niches = domain.niches.exclude(slug__in=allowed_niche_slugs)
        if removable_niches.exists():
            Book.objects.filter(niche__in=removable_niches).delete()
            BookTemplate.objects.filter(niche__in=removable_niches).delete()
            removable_niches.delete()

        for idx, niche_payload in enumerate(domain_payload['niches'], start=1):
            defaults = {
                'name': niche_payload['name'],
                'description': niche_payload['description'],
                'prompt_template': niche_payload['prompt_template'],
                'content_skeleton': niche_payload['content_skeleton'],
                'order': idx,
                'is_active': niche_payload.get('is_active', True),
            }
            Niche.objects.update_or_create(
                domain=domain,
                slug=niche_payload['slug'],
                defaults=defaults,
            )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_seed_guided_domains'),
    ]

    operations = [
        migrations.RunPython(apply_guided_catalog, noop),
    ]
