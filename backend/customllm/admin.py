from django.contrib import admin
from .models import TrainingDomain, TrainingNiche, TrainingSample, TrainingSession


@admin.register(TrainingDomain)
class TrainingDomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'training_samples_count', 'training_quality_score', 'last_trained', 'is_active']
    list_filter = ['is_active', 'last_trained']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = ['created_at', 'updated_at', 'training_samples_count', 'last_trained']


@admin.register(TrainingNiche)
class TrainingNicheAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'training_samples_count', 'is_active']
    list_filter = ['domain', 'is_active']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TrainingSample)
class TrainingSampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'niche', 'sample_type', 'quality_score', 'usage_count', 'is_active']
    list_filter = ['domain', 'sample_type', 'is_active', 'quality_score']
    search_fields = ['prompt', 'completion']
    readonly_fields = ['created_at', 'updated_at', 'usage_count', 'success_rate']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('domain', 'niche', 'sample_type', 'is_active')
        }),
        ('Training Data', {
            'fields': ('prompt', 'completion', 'context')
        }),
        ('Quality Metrics', {
            'fields': ('quality_score', 'usage_count', 'success_rate')
        }),
        ('Metadata', {
            'fields': ('source', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'status', 'samples_count', 'duration_seconds', 'started_at', 'completed_at']
    list_filter = ['status', 'domain']
    readonly_fields = ['created_at', 'started_at', 'completed_at', 'duration_seconds']
    
    fieldsets = (
        ('Session Info', {
            'fields': ('domain', 'status')
        }),
        ('Training Parameters', {
            'fields': ('samples_count', 'epochs', 'batch_size')
        }),
        ('Results', {
            'fields': ('training_loss', 'validation_accuracy')
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'duration_seconds')
        }),
        ('Logs', {
            'fields': ('log', 'error_message'),
            'classes': ('collapse',)
        }),
    )
