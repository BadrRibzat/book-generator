# Quick Integration Guide: book_generator.py

## Integrate LLM Orchestrator into Book Generation

### Current State
`books/services/book_generator.py` uses `MultiLLMOrchestrator`

### Integration Steps

1. **Import the New Orchestrator**
```python
# Replace this import:
from .multi_llm_generator import MultiLLMOrchestrator

# With:
from .llm_orchestrator import LLMOrchestrator
```

2. **Update generate_book_content() Method**

**Find (around line 150-200):**
```python
self.llm = MultiLLMOrchestrator()
outline = self.llm.generate_outline(outline_prompt)
```

**Replace with:**
```python
self.llm = LLMOrchestrator()

# Generate outline with structured context
outline = self.llm.generate_outline({
    'title': self.book.title,
    'domain': self.book.domain.name if self.book.domain else 'General',
    'niche': self.book.niche.name if self.book.niche else 'General',
    'audience': self.book.target_audience or 'General audience',
    'length': self.book.length_setting or 'medium'
})
```

3. **Update Chapter Generation with Token Validation**

**Find:**
```python
chapter_content = self.llm.generate_chapter(chapter_title, context)
```

**Replace with:**
```python
# Generate with length validation and recursive expansion
chapter_content = self.llm.generate_chapter_content(
    chapter_title=chapter_title,
    book_context={
        'title': self.book.title,
        'domain': self.book.domain.name if self.book.domain else 'General',
        'niche': self.book.niche.name if self.book.niche else 'General',
        'outline': outline,
        'previous_chapters': previous_chapters  # if tracking context
    },
    length_setting=self.book.length_setting or 'medium'
)
```

4. **Add Content Review Step (Optional)**

**After chapter generation:**
```python
# Optional: Review and refine for quality
if self.book.quality_level == 'premium':  # if you have this field
    chapter_content = self.llm.review_and_refine_content(
        content=chapter_content,
        chapter_title=chapter_title,
        book_context={'title': self.book.title}
    )
```

5. **Update PDF Generation with Dynamic Fonts**

**Find:**
```python
from .pdf_generator_pro import ProfessionalPDFGenerator
pdf_gen = ProfessionalPDFGenerator()
```

**Replace with:**
```python
from .pdf_generator_pro import ProfessionalPDFGenerator

# Generate cover brief for font selection
cover_brief = self.llm.generate_cover_brief({
    'title': self.book.title,
    'domain': self.book.domain.name,
    'niche': self.book.niche.name,
    'style': self.book.book_style.name if self.book.book_style else 'Professional'
})

# Create PDF generator with AI-selected fonts
pdf_gen = ProfessionalPDFGenerator.create_with_book_context(
    book=self.book,
    cover_brief=cover_brief
)
```

6. **Update Cover Generation (Future Enhancement)**

**When covers/services_cloudflare.py is created:**
```python
from covers.services_cloudflare import CloudflareCoverGenerator

cover_gen = CloudflareCoverGenerator()
cover_image = cover_gen.generate_ai_cover_image(
    title=self.book.title,
    brief=cover_brief,
    style=self.book.cover_style
)
```

---

## Example: Complete Integration Pattern

```python
class BookGenerator:
    def __init__(self, book):
        self.book = book
        self.llm = LLMOrchestrator()  # New orchestrator
        
    def generate_book(self):
        """Complete book generation workflow"""
        
        # Step 1: Generate outline
        outline = self.llm.generate_outline({
            'title': self.book.title,
            'domain': self.book.domain.name,
            'niche': self.book.niche.name,
            'audience': self.book.target_audience,
            'length': self.book.length_setting
        })
        
        # Step 2: Generate chapters with token validation
        chapters = []
        for chapter in outline['chapters']:
            content = self.llm.generate_chapter_content(
                chapter_title=chapter['title'],
                book_context={
                    'title': self.book.title,
                    'domain': self.book.domain.name,
                    'outline': outline
                },
                length_setting=self.book.length_setting
            )
            
            # Optional: Review for premium books
            if self.book.quality_level == 'premium':
                content = self.llm.review_and_refine_content(
                    content=content,
                    chapter_title=chapter['title'],
                    book_context={'title': self.book.title}
                )
            
            chapters.append({
                'title': chapter['title'],
                'content': content
            })
        
        # Step 3: Generate cover brief for font selection
        cover_brief = self.llm.generate_cover_brief({
            'title': self.book.title,
            'domain': self.book.domain.name,
            'niche': self.book.niche.name,
            'style': self.book.book_style.name
        })
        
        # Step 4: Create PDF with dynamic fonts
        pdf_gen = ProfessionalPDFGenerator.create_with_book_context(
            book=self.book,
            cover_brief=cover_brief
        )
        
        pdf_path = pdf_gen.create_ebook(
            title=self.book.title,
            chapters=chapters,
            author=self.book.author_name
        )
        
        return pdf_path
```

---

## Testing Integration

```bash
# Activate virtual environment
cd /home/badr/book-generator/backend && source venv/bin/activate

# Test book generation
python manage.py shell

>>> from books.models import Book, Domain, Niche
>>> from books.services.book_generator import BookGenerator
>>> 
>>> # Create test book
>>> domain = Domain.objects.get(slug='ai_automation')
>>> niche = Niche.objects.get(slug='workflow_automation')
>>> book = Book.objects.create(
...     title='AI Automation Guide',
...     domain=domain,
...     niche=niche,
...     length_setting='medium'
... )
>>> 
>>> # Generate book
>>> generator = BookGenerator(book)
>>> pdf_path = generator.generate_book()
>>> print(f"Generated: {pdf_path}")
```

---

## Rollback Plan

If issues occur, the `MultiLLMOrchestrator` wrapper ensures backward compatibility:

```python
# LLMOrchestrator provides backward-compatible interface
from .llm_orchestrator import MultiLLMOrchestrator  # wrapper class

# Works with old code:
llm = MultiLLMOrchestrator()
outline = llm.generate_outline(prompt_string)  # still works!
```

---

## Monitoring

After integration, monitor these metrics:

1. **Token Usage**: Check `token_usage.json` for per-model consumption
2. **Generation Time**: Track time for outline vs chapters
3. **Font Selection**: Log which themes are selected most
4. **Cost**: Monitor Cloudflare usage (images + token counting)
5. **Quality**: Compare content length against thresholds

---

## Support

For issues during integration:
- Check `IMPLEMENTATION_SUMMARY.md` for complete architecture
- Review `test_enhanced_system.py` for usage examples
- Test LLM orchestrator in isolation before full integration
- Ensure `.env` has valid OpenRouter API key

---

**Last Updated:** October 27, 2025
