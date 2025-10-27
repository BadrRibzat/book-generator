"""
Test Custom LLM Model
Management command to test Cloudflare integration and custom model
"""

from django.core.management.base import BaseCommand
from customllm.services.model_service import CustomModelService
import json


class Command(BaseCommand):
    help = 'Test custom LLM model integration with Cloudflare'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== Testing Custom LLM Model ===\n'))
        
        try:
            # Initialize service
            service = CustomModelService()
            
            # Test 1: Connection test
            self.stdout.write('1. Testing Cloudflare connection...')
            test_result = service.test_model()
            
            if test_result.get('success'):
                self.stdout.write(self.style.SUCCESS(f'   ✓ Connection successful'))
                self.stdout.write(f'   Model: {test_result.get("model")}')
                self.stdout.write(f'   Response time: {test_result.get("elapsed_time", 0):.2f}s')
                self.stdout.write(f'   Response preview: {test_result.get("response", "")[:100]}...')
            else:
                self.stdout.write(self.style.ERROR(f'   ✗ Connection failed: {test_result.get("error")}'))
                return
            
            self.stdout.write('')
            
            # Test 2: Outline generation
            self.stdout.write('2. Testing outline generation...')
            outline_result = service.generate_book_outline(
                domain="AI & Automation",
                niche="No-Code AI Tools",
                target_audience="beginners",
                page_count=20
            )
            
            self.stdout.write(self.style.SUCCESS(f'   ✓ Outline generated'))
            self.stdout.write(f'   Title: {outline_result.get("outline", {}).get("title")}')
            self.stdout.write(f'   Chapters: {outline_result.get("chapters")}')
            self.stdout.write(f'   Time: {outline_result.get("metadata", {}).get("elapsed_time", 0):.2f}s')
            
            self.stdout.write('')
            
            # Test 3: Chapter generation
            self.stdout.write('3. Testing chapter generation...')
            chapter_result = service.generate_chapter_content(
                chapter_title="Introduction to No-Code AI",
                chapter_outline="Overview of no-code AI tools and their benefits",
                book_context={
                    'domain': 'AI & Automation',
                    'niche': 'No-Code AI Tools',
                    'target_audience': 'beginners'
                },
                word_count=500
            )
            
            self.stdout.write(self.style.SUCCESS(f'   ✓ Chapter generated'))
            self.stdout.write(f'   Word count: {chapter_result.get("word_count")}')
            self.stdout.write(f'   Time: {chapter_result.get("metadata", {}).get("elapsed_time", 0):.2f}s')
            self.stdout.write(f'   Preview: {chapter_result.get("content", "")[:150]}...')
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=== All Tests Passed ===\n'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Test failed: {str(e)}\n'))
            import traceback
            traceback.print_exc()
