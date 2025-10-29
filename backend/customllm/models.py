"""
Custom LLM Training Data Models
Stores domain-specific training data in MongoDB via Django
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TrainingDomain(models.Model):
    """
    Predefined domains for custom LLM training.
    Domains now sync with the guided catalog and can grow beyond the original trio.
    """

    slug = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Training statistics
    training_samples_count = models.IntegerField(default=0)
    last_trained = models.DateTimeField(null=True, blank=True)
    training_quality_score = models.FloatField(default=0.0)  # 0-100
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customllm_training_domains'
        verbose_name = 'Training Domain'
        verbose_name_plural = 'Training Domains'
    
    def __str__(self):
        return self.name


class TrainingNiche(models.Model):
    """
    Specific niches within each domain for targeted training
    """
    domain = models.ForeignKey(TrainingDomain, on_delete=models.CASCADE, related_name='niches')
    slug = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Keywords and context for training
    keywords = models.JSONField(default=list)  # List of relevant keywords
    target_audiences = models.JSONField(default=list)  # e.g., ['beginners', 'professionals']
    
    training_samples_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customllm_training_niches'
        verbose_name = 'Training Niche'
        verbose_name_plural = 'Training Niches'
        unique_together = ['domain', 'slug']
    
    def __str__(self):
        return f"{self.domain.name} - {self.name}"


class TrainingSample(models.Model):
    """
    Training data for custom LLM model
    Stores prompt-completion pairs for fine-tuning
    """
    SAMPLE_TYPES = [
        ('outline', 'Book Outline'),
        ('chapter', 'Chapter Content'),
        ('introduction', 'Introduction'),
        ('conclusion', 'Conclusion'),
        ('cover_description', 'Cover Description'),
    ]
    
    domain = models.ForeignKey(TrainingDomain, on_delete=models.CASCADE, related_name='samples')
    niche = models.ForeignKey(TrainingNiche, on_delete=models.CASCADE, related_name='samples')
    
    sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPES)
    
    # Training pair
    prompt = models.TextField(help_text="Input prompt for the model")
    completion = models.TextField(help_text="Expected output/completion")
    
    # Metadata
    context = models.JSONField(default=dict, help_text="Additional context (audience, length, style, etc.)")
    quality_score = models.FloatField(default=1.0, help_text="Quality rating 0-1")
    
    # Usage tracking
    usage_count = models.IntegerField(default=0, help_text="Times used in training")
    success_rate = models.FloatField(default=0.0, help_text="Success rate when used")
    
    # Source tracking
    source = models.CharField(max_length=50, default='manual', help_text="manual, generated, imported")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customllm_training_samples'
        verbose_name = 'Training Sample'
        verbose_name_plural = 'Training Samples'
        indexes = [
            models.Index(fields=['domain', 'niche', 'sample_type']),
            models.Index(fields=['quality_score']),
        ]
    
    def __str__(self):
        return f"{self.domain.slug} - {self.sample_type} - {self.prompt[:50]}..."


class TrainingSession(models.Model):
    """
    Records of training sessions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    domain = models.ForeignKey(TrainingDomain, on_delete=models.CASCADE, related_name='training_sessions', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Training parameters
    samples_count = models.IntegerField(default=0)
    epochs = models.IntegerField(default=1)
    batch_size = models.IntegerField(default=8)
    
    # Results
    training_loss = models.FloatField(null=True, blank=True)
    validation_accuracy = models.FloatField(null=True, blank=True)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    
    # Logs
    log = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'customllm_training_sessions'
        verbose_name = 'Training Session'
        verbose_name_plural = 'Training Sessions'
        ordering = ['-created_at']
    
    def __str__(self):
        domain_name = self.domain.name if self.domain else "All Domains"
        return f"Training: {domain_name} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

# Create your models here.
