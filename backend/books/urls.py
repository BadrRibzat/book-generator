# books/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'domains', views.DomainViewSet, basename='domain')
router.register(r'niches', views.NicheViewSet, basename='niche')
router.register(r'book-styles', views.BookStyleViewSet, basename='book-style')
router.register(r'cover-styles', views.CoverStyleViewSet, basename='cover-style')

urlpatterns = [
    path('books/create-guided/', views.create_guided_book, name='create-guided-book'),
    path('', include(router.urls)),
]
