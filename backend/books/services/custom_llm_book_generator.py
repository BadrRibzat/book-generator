"""
Custom LLM Book Generator
Uses ONLY local trained LLM - completely replaces OpenRouter system
Unlimited generation for AI & Automation, Parenting, E-commerce domains
"""

import logging
from typing import Dict, Any
from django.utils import timezone
from pathlib import Path

from customllm.services.custom_book_generator import CustomBookGenerator
from books.services.pdf_generator_pro import ProfessionalPDFGenerator
from backend.utils.mongodb import get_mongodb_db

logger = logging.getLogger(__name__)


class CustomLLMBookGenerator:
    """
    Complete book generation using custom trained LLM
    - NO OpenRouter API calls
    - NO rate limits
    - Instant generation
    - Only Cloudflare for cover images
    """
    
    def __init__(self):
        self.custom_llm = CustomBookGenerator()
        self.pdf_generator = ProfessionalPDFGenerator()
    
    def generate_book_content(self, book) -> Dict[str, Any]:
        """
        Generate complete book content using custom LLM
        
        Args:
            book: Book model instance
        
        Returns:
            Dict with all book content
        """
        try:
            logger.info(f"📚 Generating book with Custom LLM: {book.title}")
            
            # Prepare book context
            book_length = book.book_style.length if book.book_style else 'medium'
            target_audience = book.book_style.target_audience if book.book_style else 'professionals'
            
            book_context = {
                'domain': book.domain.name if book.domain else 'AI & Automation',
                'niche': book.niche.name if book.niche else 'General',
                'audience': target_audience,
                'page_count': self._calculate_page_count(book_length),
                'title': book.title or 'Complete Guide',
                'style': book.book_style.tone if book.book_style else 'professional'
            }
            
            # Validate domain is supported
            if not self.custom_llm.is_domain_supported(book_context['domain']):
                raise ValueError(
                    f"Domain '{book_context['domain']}' not supported. "
                    f"Supported domains: {', '.join(self.custom_llm.get_supported_domains())}"
                )
            
            # Step 1: Generate outline
            logger.info("📝 Step 1/3: Generating outline...")
            book.current_step = 'Generating book outline'
            book.progress_percentage = 20
            book.save()
            
            outline_result = self.custom_llm.generate_book_outline(book_context)
            outline = outline_result['outline']
            chapters_list = outline.get('chapters', [])
            
            logger.info(f"✅ Outline generated: {len(chapters_list)} chapters")
            
            # Step 2: Generate chapters
            logger.info(f"✍️ Step 2/3: Generating {len(chapters_list)} chapters...")
            chapters_content = []
            
            for i, chapter_info in enumerate(chapters_list, 1):
                progress = 30 + (i * 40 // len(chapters_list))  # 30-70%
                book.current_step = f'Generating chapter {i}/{len(chapters_list)}: {chapter_info["title"]}'
                book.progress_percentage = progress
                book.save()
                
                logger.info(f"   Chapter {i}/{len(chapters_list)}: {chapter_info['title']}")
                
                chapter_result = self.custom_llm.generate_chapter(
                    chapter_title=chapter_info['title'],
                    chapter_outline=chapter_info.get('summary', ''),
                    book_context=book_context,
                    word_count=self._calculate_chapter_word_count(book_length)
                )
                
                chapters_content.append({
                    'number': i,
                    'title': chapter_info['title'],
                    'content': chapter_result['content'],
                    'word_count': chapter_result['word_count']
                })
            
            logger.info(f"✅ All {len(chapters_content)} chapters generated")
            
            # Step 3: Compile final content
            logger.info("📦 Step 3/3: Compiling final content...")
            book.current_step = 'Compiling book content'
            book.progress_percentage = 75
            book.save()
            
            content_data = {
                'title': outline.get('title', book.title),
                'outline': outline,
                'chapters': chapters_content,
                'metadata': {
                    'domain': book_context['domain'],
                    'niche': book_context['niche'],
                    'audience': book_context['audience'],
                    'total_chapters': len(chapters_content),
                    'total_words': sum(ch['word_count'] for ch in chapters_content),
                    'generated_with': 'custom_local_llm',
                    'generation_time': outline_result['metadata']['elapsed_time'],
                    'api_calls_used': 0  # Zero external API calls for text!
                }
            }
            
            logger.info(f"✅ Book content generated: {content_data['metadata']['total_words']} words")
            
            return content_data
            
        except Exception as e:
            logger.error(f"❌ Book generation failed: {str(e)}")
            raise
    
    def create_pdf(self, book, content_data: Dict[str, Any]) -> str:
        """
        Create PDF using ReportLab
        
        Args:
            book: Book model instance
            content_data: Generated content
        
        Returns:
            Path to created PDF
        """
        try:
            logger.info("📄 Creating PDF with ReportLab...")
            
            # Generate output path
            from django.conf import settings
            media_root = Path(settings.MEDIA_ROOT)
            books_dir = media_root / 'books'
            books_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = str(books_dir / f'book_{book.id}_interior.pdf')
            
            # Use professional PDF generator
            self.pdf_generator.create_book_pdf(
                book=book,
                content_data=content_data,
                output_path=output_path
            )
            
            logger.info(f"✅ PDF created: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"❌ PDF creation failed: {str(e)}")
            raise
    
    def save_to_mongodb(self, book_id: int, content_data: Dict[str, Any], interior_pdf_path: str) -> str:
        """
        Save book content to MongoDB
        
        Args:
            book_id: Book ID
            content_data: Content data
            interior_pdf_path: Path to PDF
        
        Returns:
            MongoDB document ID
        """
        try:
            db = get_mongodb_db()
            collection = db['book_contents']
            
            document = {
                'book_id': book_id,
                'content': content_data,
                'interior_pdf_path': interior_pdf_path,
                'generated_with': 'custom_local_llm',
                'external_api_calls': 0,  # Zero API calls for text generation!
                'created_at': timezone.now().isoformat()
            }
            
            result = collection.insert_one(document)
            logger.info(f"✅ Content saved to MongoDB: {result.inserted_id}")
            
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ MongoDB save failed: {str(e)}")
            raise
    
    def _calculate_page_count(self, book_length: str) -> int:
        """Calculate target page count based on book length"""
        length_mapping = {
            'short': 15,
            'medium': 25,
            'long': 35,
            'full': 45
        }
        return length_mapping.get(book_length, 25)
    
    def _calculate_chapter_word_count(self, book_length: str) -> int:
        """Calculate target word count per chapter"""
        length_mapping = {
            'short': 400,
            'medium': 600,
            'long': 800,
            'full': 1000
        }
        return length_mapping.get(book_length, 600)
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get generation statistics"""
        return self.custom_llm.get_training_stats()
