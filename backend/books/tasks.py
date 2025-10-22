# books/tasks.py
"""
Celery tasks for book generation pipeline
"""

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from pathlib import Path
import logging

from .models import Book
from .services.book_generator import BookGeneratorProfessional
from .services.pdf_merger import PDFMerger
from covers.services import CoverGeneratorProfessional
from backend.utils.mongodb import get_mongodb_db

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def generate_book_content(self, book_id):
    """
    Generate book content using AI and create interior PDF
    """
    try:
        # Get book instance
        book = Book.objects.get(id=book_id)

        # Update status
        book.status = 'generating'
        book.save()

        logger.info(f"Starting content generation for book {book_id}: {book.title}")

        # Generate content using the updated book generator
        generator = BookGeneratorProfessional()
        content_data = generator.generate_book_content(book)

        # Create interior PDF
        interior_pdf_path = generator.create_pdf(book, content_data)

        # Store content in MongoDB
        db = get_mongodb_db()
        result = db.book_contents.insert_one({
            'book_id': book.id,
            'content': content_data,
            'interior_pdf_path': interior_pdf_path,
            'created_at': timezone.now().isoformat()
        })

        # Update book
        book.mongodb_id = str(result.inserted_id)
        book.status = 'content_generated'
        book.content_generated_at = timezone.now()
        book.save()

        logger.info(f"Content generation completed for book {book_id}")

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
    Generate 3 cover options for the book
    """
    try:
        # Get book instance
        book = Book.objects.get(id=book_id)

        # Ensure content is generated first
        if book.status != 'content_generated':
            logger.warning(f"Cannot generate covers for book {book_id}: content not ready")
            return {'status': 'skipped', 'book_id': book_id, 'reason': 'content_not_ready'}

        logger.info(f"Starting cover generation for book {book_id}: {book.title}")

        # Generate covers
        cover_gen = CoverGeneratorProfessional()
        covers = cover_gen.generate_three_covers(book)

        if len(covers) == 0:
            raise Exception("No covers were generated")

        logger.info(f"Successfully generated {len(covers)} covers for book {book_id}")

        # Update book status
        book.status = 'cover_pending'
        book.save()

        return {'status': 'success', 'book_id': book_id, 'covers_count': len(covers)}

    except Exception as e:
        logger.error(f"Cover generation failed for book {book_id}: {str(e)}")

        # Update book status
        try:
            book = Book.objects.get(id=book_id)
            book.status = 'error'
            book.error_message = f"Cover generation failed: {str(e)}"
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
            generator = BookGeneratorProfessional()
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