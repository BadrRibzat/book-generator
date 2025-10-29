from django.contrib import admin
from .models import Book, BookTemplate, Domain, Niche, CoverStyle


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Niche)
class NicheAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'is_active', 'order']
    list_filter = ['domain', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['domain', 'order', 'name']


@admin.register(CoverStyle)
class CoverStyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'style', 'is_active', 'order']
    list_filter = ['style', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'domain', 'niche', 'book_length', 'status', 'quality_score', 'created_at']
    list_filter = ['status', 'domain', 'niche', 'book_length', 'created_at']
    search_fields = ['title', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'generation_started_at', 'generation_completed_at']
    ordering = ['-created_at']


@admin.register(BookTemplate)
class BookTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'domain', 'niche', 'is_public', 'usage_count']
    list_filter = ['is_public', 'is_featured', 'domain']
    search_fields = ['name', 'description', 'user__username']
    ordering = ['-created_at']
