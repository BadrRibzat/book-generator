from django.db import migrations, models
import django.db.models.deletion


def migrate_book_length(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    BookStyle = apps.get_model('books', 'BookStyle')

    length_map = {
        'short': 'short',
        'medium': 'standard',
        'full': 'long',
    }

    for book in Book.objects.all().iterator():
        book_length = 'standard'

        if book.book_style_id:
            try:
                style = BookStyle.objects.get(pk=book.book_style_id)
                book_length = length_map.get(style.length, 'standard')
            except BookStyle.DoesNotExist:
                book_length = 'standard'

        book.book_length = book_length
        book.save(update_fields=['book_length'])


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_quality_score'),
    ]

    operations = [
        # Niche metadata updates
        migrations.RemoveField(
            model_name='niche',
            name='audience',
        ),
        migrations.RemoveField(
            model_name='niche',
            name='market_size',
        ),
        migrations.AddField(
            model_name='niche',
            name='content_skeleton',
            field=models.JSONField(default=list, help_text='Ordered outline the generator must follow for this niche'),
        ),
        migrations.AddField(
            model_name='niche',
            name='prompt_template',
            field=models.TextField(blank=True, default='', help_text='Prompt template injected into the LLM for this niche'),
        ),

        # Book workflow updates
        migrations.AddField(
            model_name='book',
            name='book_length',
            field=models.CharField(choices=[('short', 'Short (~20-25 pages)'), ('standard', 'Standard (~35-45 pages)'), ('long', 'Long (~50-70 pages)')], default='standard', help_text='Driving page count and chapter depth', max_length=15),
        ),
        migrations.RunPython(migrate_book_length, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='book',
            name='book_style',
        ),
        migrations.DeleteModel(
            name='BookStyle',
        ),
        migrations.AlterField(
            model_name='book',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='books.domain'),
        ),
        migrations.AlterField(
            model_name='book',
            name='niche',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='books.niche'),
        ),
    ]
