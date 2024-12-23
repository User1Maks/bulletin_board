from django.contrib import admin

from ads.models import Ad, Review


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Выводит отображение объектов модели объявлений в django-admin"""
    list_display = ('id', 'title', 'price', 'description', 'author',
                    'created_at', 'updated_at',)
    search_fields = ('title',)
    list_filter = ('title', 'price', 'author', 'created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Выводит отображение объектов модели отзывов в django-admin"""
    list_display = ('id', 'text', 'author', 'ad', 'created_at', 'updated_at',)
    search_fields = ('author', 'ad',)
    list_filter = ('author',)
