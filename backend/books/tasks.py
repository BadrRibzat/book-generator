# books/tasks.py
"""
Celery tasks for book generation pipeline
Uses Custom LLM - NO OpenRouter, NO rate limits
"""

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from pathlib import Path
import logging

from .models import Book
from .services.custom_llm_book_generator import CustomLLMBookGenerator  # NEW: Custom LLM
from .services.pdf_merger import PDFMerger
from covers.services_pro import CoverGeneratorProfessional
from backend.utils.mongodb import get_mongodb_db

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def generate_book_content(self, book_id):
    """
    Generate book content using Custom LLM (NO OpenRouter)
    Unlimited generation with no rate limits
    """
    try:
        # Get book instance with related objects
        book = Book.objects.select_related('domain', 'niche', 'user').get(id=book_id)

        # Update status and progress
        book.status = 'generating'
        book.progress_percentage = 10
        book.current_step = 'Initializing custom LLM generation'
        book.save()

        logger.info(f"🚀 Starting CUSTOM LLM generation for book {book_id}: {book.title}")

        # Update progress
        book.progress_percentage = 15
        book.current_step = 'Using custom trained model (no API limits)'
        book.save()

        # Generate content using CUSTOM LLM (NO external APIs)
        generator = CustomLLMBookGenerator()
        content_data = generator.generate_book_content(book)

        # Update book title with the generated title
        generated_title = content_data.get('title', 'Complete Guide')
        if generated_title and generated_title != 'Generating...':
            book.title = generated_title
            logger.info(f"📚 Updated book title to: {generated_title}")

        # Update progress
        book.progress_percentage = 70
        book.current_step = 'Creating interior PDF with ReportLab'
        book.save()

        # Create interior PDF
        interior_pdf_path = generator.create_pdf(book, content_data)

        # Update progress
        book.progress_percentage = 80
        book.current_step = 'Storing content in database'
        book.save()

        # Store content in MongoDB
        mongodb_id = generator.save_to_mongodb(book.id, content_data, interior_pdf_path)

        # Update book
        book.mongodb_id = mongodb_id
        book.status = 'content_generated'
        book.content_generated_at = timezone.now()
        book.progress_percentage = 90
        book.current_step = 'Content generation completed - NO API limits used!'
        book.save()

        logger.info(f"✅ CUSTOM LLM generation completed for book {book_id}")
        logger.info(f"   Words: {content_data['metadata']['total_words']}")
        logger.info(f"   Chapters: {content_data['metadata']['total_chapters']}")
        logger.info(f"   External API calls: {content_data['metadata']['api_calls_used']}")

        # Trigger cover generation
        generate_book_covers.delay(book_id)

        return {'status': 'success', 'book_id': book_id}

    except Exception as e:
        logger.error(f"Content generation failed for book {book_id}: {str(e)}")

        # Update book status
        try:
            book = Book.objects.get(id=book_id)
            book.status = 'error'
            book.error_message = str(e)
            book.progress_percentage = 0
            book.current_step = f'Error: {str(e)}'
            book.save()
        except Exception:
            pass

        # Retry with exponential backoff
        if self.request.retries < self.max_retries:
            delay = 2 ** self.request.retries  # 2, 4, 8 seconds
            logger.info(f"Retrying content generation for book {book_id} in {delay} seconds")
            raise self.retry(countdown=delay, exc=e)

        return {'status': 'failed', 'book_id': book_id, 'error': str(e)}


@shared_task(bind=True, max_retries=2)
def generate_book_covers(self, book_id):
    """
    Generate cover for the book - single cover for guided workflow, multiple for manual
    """
    try:
        print(f"DEBUG: generate_book_covers task started for book_id {book_id}")
        
        # Get book instance with related objects
        book = Book.objects.select_related('domain', 'niche', 'user').get(id=book_id)

        print(f"DEBUG: Book object retrieved: {book}")
        print(f"DEBUG: book.id = {book.id}")
        print(f"DEBUG: book.title = {book.title}")
        print(f"DEBUG: book.domain = {book.domain}")
        print(f"DEBUG: book.domain_id = {book.domain_id}")
        print(f"DEBUG: book.niche = {book.niche}")
        print(f"DEBUG: book.niche_id = {book.niche_id}")
        print(f"DEBUG: book.status = {book.status}")

        # DEBUG: Check book object
        logger.info(f"DEBUG: Book {book_id} loaded")
        logger.info(f"DEBUG: book.domain = {book.domain}")
        logger.info(f"DEBUG: book.domain_id = {book.domain_id}")
        logger.info(f"DEBUG: book.niche = {book.niche}")
        logger.info(f"DEBUG: book.niche_id = {book.niche_id}")
        logger.info(f"DEBUG: is_guided = {book.domain_id is not None and book.niche_id is not None}")

        # Ensure content is generated first
        if book.status != 'content_generated':
            logger.warning(f"Cannot generate covers for book {book_id}: content not ready")
            return {'status': 'skipped', 'book_id': book_id, 'reason': 'content_not_ready'}

        # Update progress
        book.progress_percentage = 92
        book.current_step = 'Starting cover generation'
        book.save()

        logger.info(f"Starting cover generation for book {book_id}: {book.title}")

        # Guided workflow requires domain + niche selection
        is_guided = book.domain_id is not None and book.niche_id is not None

        if is_guided:
            # Update progress
            book.progress_percentage = 94
            book.current_step = 'Generating cover for guided book'
            book.save()

            # Generate single cover for guided workflow
            cover_gen = CoverGeneratorProfessional()
            cover = cover_gen.generate_single_cover(book)

            # Update progress
            book.progress_percentage = 98
            book.current_step = 'Cover generated, preparing final PDF'
            book.save()
            
            logger.info(f"Successfully generated single cover for guided book {book_id}")
            
            # For guided workflow, automatically create final PDF
            create_final_book_pdf.delay(book_id)
            
            return {'status': 'success', 'book_id': book_id, 'covers_count': 1, 'guided': True}
        else:
            # Update progress
            book.progress_percentage = 94
            book.current_step = 'Generating cover options'
            book.save()

            # Generate 3 covers for manual workflow
            cover_gen = CoverGeneratorProfessional()
            covers = cover_gen.generate_three_covers(book)
            
            if len(covers) == 0:
                raise Exception("No covers were generated")

            # Update progress
            book.progress_percentage = 96
            book.current_step = 'Cover options generated'
            book.save()
            
            logger.info(f"Successfully generated {len(covers)} covers for manual book {book_id}")
            
            # Update book status
            book.status = 'cover_pending'
            book.save()
            
            return {'status': 'success', 'book_id': book_id, 'covers_count': len(covers), 'guided': False}

    except Exception as e:
        logger.error(f"Cover generation failed for book {book_id}: {str(e)}")

        # Update book status
        try:
            book = Book.objects.get(id=book_id)
            book.status = 'error'
            book.error_message = f"Cover generation failed: {str(e)}"
            book.progress_percentage = 0
            book.current_step = f'Error: {str(e)}'
            book.save()
        except Exception:
            pass

        # Retry
        if self.request.retries < self.max_retries:
            delay = 5 * (self.request.retries + 1)  # 5, 10 seconds
            logger.info(f"Retrying cover generation for book {book_id} in {delay} seconds")
            raise self.retry(countdown=delay, exc=e)

        return {'status': 'failed', 'book_id': book_id, 'error': str(e)}


@shared_task(bind=True, max_retries=2)
def create_final_book_pdf(self, book_id):
    """
    Merge selected cover with interior PDF to create final downloadable book
    """
    try:
        # Get book instance
        book = Book.objects.get(id=book_id)

        # Ensure cover is selected
        if not book.selected_cover:
            logger.warning(f"Cannot create final PDF for book {book_id}: no cover selected")
            return {'status': 'skipped', 'book_id': book_id, 'reason': 'no_cover_selected'}

        # Update progress
        book.progress_percentage = 98
        book.current_step = 'Preparing final PDF creation'
        book.save()

        logger.info(f"Creating final PDF for book {book_id}: {book.title}")

        # Get interior PDF path from MongoDB
        db = get_mongodb_db()
        content_doc = db.book_contents.find_one({'book_id': book.id})

        if not content_doc:
            raise Exception("Book content not found in MongoDB")

        interior_pdf_path = content_doc.get('interior_pdf_path')
        if not interior_pdf_path:
            raise Exception("Interior PDF path not found")

        # Check if interior PDF exists
        if not Path(interior_pdf_path).exists():
            # Try to regenerate if missing
            logger.warning(f"Interior PDF missing for book {book_id}, attempting regeneration")
            book.progress_percentage = 99
            book.current_step = 'Regenerating interior PDF'
            book.save()

            generator = CustomLLMBookGenerator()  # Use Custom LLM
            content_data = content_doc.get('content', {})
            if content_data:
                interior_pdf_path = generator.create_pdf(book, content_data)
                # Update MongoDB
                db.book_contents.update_one(
                    {'book_id': book.id},
                    {'$set': {'interior_pdf_path': interior_pdf_path}}
                )
            else:
                raise Exception("No content data available to regenerate PDF")

        # Update progress
        book.progress_percentage = 99
        book.current_step = 'Merging cover with content'
        book.save()

        # Merge with selected cover
        merger = PDFMerger()
        final_pdf_path = merger.merge_book(book, interior_pdf_path, book.selected_cover)

        # Update MongoDB and book model
        db.book_contents.update_one(
            {'book_id': book.id},
            {'$set': {'final_pdf_path': final_pdf_path}}
        )

        book.final_pdf_path = final_pdf_path
        book.status = 'ready'
        book.progress_percentage = 100
        book.current_step = 'Book completed and ready for download'
        book.save()

        logger.info(f"Final PDF created successfully for book {book_id}")

        return {'status': 'success', 'book_id': book_id, 'final_pdf_path': final_pdf_path}

    except Exception as e:
        logger.error(f"Final PDF creation failed for book {book_id}: {str(e)}")

        # Update book status
        try:
            book = Book.objects.get(id=book_id)
            book.status = 'error'
            book.error_message = f"PDF creation failed: {str(e)}"
            book.progress_percentage = 0
            book.current_step = f'Error: {str(e)}'
            book.save()
        except Exception:
            pass

        # Retry
        if self.request.retries < self.max_retries:
            delay = 3 * (self.request.retries + 1)  # 3, 6 seconds
            logger.info(f"Retrying final PDF creation for book {book_id} in {delay} seconds")
            raise self.retry(countdown=delay, exc=e)

        return {'status': 'failed', 'book_id': book_id, 'error': str(e)}


@shared_task
def cleanup_old_books():
    """
    Periodic task to clean up old draft/error books and temporary files
    """
    try:
        # Delete books older than 30 days that are in draft/error status
        cutoff_date = timezone.now() - timezone.timedelta(days=30)

        old_books = Book.objects.filter(
            created_at__lt=cutoff_date,
            status__in=['draft', 'error']
        )

        deleted_count = 0
        for book in old_books:
            try:
                # Delete associated files
                if book.final_pdf_path and Path(book.final_pdf_path).exists():
                    Path(book.final_pdf_path).unlink()

                # Delete from MongoDB
                if book.mongodb_id:
                    db = get_mongodb_db()
                    db.book_contents.delete_one({'book_id': book.id})

                # Delete covers
                book.covers.all().delete()

                # Delete book
                book.delete()
                deleted_count += 1

            except Exception as e:
                logger.error(f"Error deleting book {book.id}: {str(e)}")

        logger.info(f"Cleaned up {deleted_count} old books")

        return {'status': 'success', 'deleted_count': deleted_count}

    except Exception as e:
        logger.error(f"Cleanup task failed: {str(e)}")
        return {'status': 'failed', 'error': str(e)}