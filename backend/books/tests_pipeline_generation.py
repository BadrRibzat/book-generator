from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Domain, Niche, BookStyle, Book
from books.services.custom_llm_book_generator import CustomLLMBookGenerator


class PipelineGenerationTests(TestCase):
    def setUp(self):
        # Minimal fixtures
        self.user = User.objects.create_user(username='tester', password='x')
        self.domain = Domain.objects.create(name='AI & Automation', slug='ai_automation')
        self.niche = Niche.objects.create(domain=self.domain, name='ChatGPT and AI Tools for Productivity', slug='chatgpt_productivity')
        self.style = BookStyle.objects.create(
            name='Pro Medium', tone='professional', target_audience='professionals', language='en', length='medium', is_active=True
        )

    def test_custom_llm_pipeline_generates_high_quality_book(self):
        # Create Book
        book = Book.objects.create(
            user=self.user,
            title='AI Productivity Playbook',
            domain=self.domain,
            niche=self.niche,
            book_style=self.style,
            status='draft'
        )

        generator = CustomLLMBookGenerator()
        content = generator.generate_book_content(book)

        # Basic structure assertions
        self.assertIn('chapters', content)
        self.assertGreaterEqual(len(content['chapters']), 6)

        # Quality assertion: with full training data the pipeline enforces >=80.
        # In test (no training samples), fallback generation should still be healthy (>=60).
        quality = content['metadata'].get('quality', {})
        avg = quality.get('average_score', 0)
        self.assertGreaterEqual(avg, 60, f"Expected >=60 average quality in fallback mode, got {avg}")

        # Heading structure present (#### subtopic sections)
        any_headings = any('####' in ch.get('content', '') for ch in content['chapters'])
        self.assertTrue(any_headings)
