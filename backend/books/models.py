from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    """
    Main Book model - stores metadata in SQLite, content in MongoDB
    Status flow: draft -> content_generated -> cover_pending -> ready
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generating', 'Generating Content'),
        ('content_generated', 'Content Generated'),
        ('cover_pending', 'Awaiting Cover Selection'),
        ('ready', 'Ready for Download'),
        ('error', 'Generation Error'),
    ]
    
    DOMAIN_CHOICES = [
        ('language_kids', 'Language and Kids'),
        ('tech_ai', 'Technology and AI'),
        ('nutrition', 'Nutrition and Wellness'),
        ('meditation', 'Meditation'),
        ('home_workout', 'Home Workout'),
    ]
    
    SUB_NICHE_CHOICES = [
        # Language and Kids
        ('ai_learning_stories', 'AI-Powered Personalized Learning Stories'),
        ('multilingual_coloring', 'Multilingual Coloring Books'),
        ('kids_mindful_journals', 'Kids\' Mindful Activity Journals'),
        
        # Technology and AI
        ('ai_ethics', 'AI Ethics and Future Trends'),
        ('nocode_guides', 'No-Code/Low-Code Development Guides'),
        ('smart_home_diy', 'DIY Smart Home and Automation'),
        
        # Nutrition and Wellness
        ('specialty_diet', 'Specialty Diet Cookbooks'),
        ('plant_based_cooking', 'Plant-Based Cooking for Beginners'),
        ('nutrition_mental_health', 'Nutrition for Mental Health'),
        
        # Meditation
        ('mindfulness_anxiety', 'Mindfulness and Anxiety Workbooks'),
        ('sleep_meditation', 'Sleep Meditation Stories'),
        ('gratitude_journals', 'Daily Gratitude Journals with Prompts'),
        
        # Home Workout
        ('equipment_free', 'Equipment-Free Workout Plans'),
        ('yoga_remote_workers', 'Yoga and Stretching for Remote Workers'),
        ('mobility_training', 'Beginner\'s Mobility Training'),
    ]
    
    PAGE_LENGTH_CHOICES = [
        (15, '15 Pages'),
        (20, '20 Pages'),
        (25, '25 Pages'),
        (30, '30 Pages'),
    ]
    
    # Core fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)  # Auto-generated
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    sub_niche = models.CharField(max_length=50, choices=SUB_NICHE_CHOICES)
    page_length = models.IntegerField(choices=PAGE_LENGTH_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # MongoDB reference for content
    mongodb_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_generated_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Error tracking
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"
    
    def can_download(self):
        """Check if book is ready for download"""
        return self.status == 'ready' and self.selected_cover is not None
    
    @property
    def selected_cover(self):
        """Get the selected cover for this book"""
        return self.covers.filter(is_selected=True).first()
