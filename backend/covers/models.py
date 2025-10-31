from django.db import models
from books.models import Book

class Cover(models.Model):
    """Cover model storing generated design variants per book."""

    # Relationships
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='covers')
    
    # Cover details
    template_style = models.CharField(
        max_length=80,
        help_text="Identifier for the dynamic template or trend used to render the cover",
    )
    image_path = models.CharField(max_length=500)  # Path to generated cover image
    pdf_path = models.CharField(max_length=500, blank=True, null=True)  # Path to cover PDF
    
    # Selection status
    is_selected = models.BooleanField(default=False)
    
    # Generation metadata
    generation_params = models.JSONField(default=dict)  # Store colors, fonts, etc.
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['book', '-created_at']),
        ]
    
    def __str__(self):
        return f"Cover {self.id} for {self.book.title} ({'Selected' if self.is_selected else 'Option'})"
    
    def select(self):
        """Select this cover and deselect all others for this book"""
        # Deselect all other covers for this book
        Cover.objects.filter(book=self.book).update(is_selected=False)
        # Select this one
        self.is_selected = True
        self.save()
        
        # Update book status to ready if content is generated
        if self.book.status == 'cover_pending':
            from django.utils import timezone
            self.book.status = 'ready'
            self.book.completed_at = timezone.now()
            self.book.save()
