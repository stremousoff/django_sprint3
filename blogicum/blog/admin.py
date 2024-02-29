from django.contrib import admin

from .models import Category, Location, Post


class PostAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Post."""

    list_display = (
        'title',
        'text_short',
        'location',
        'category',
        'pub_date',
        'is_published',
    )
    list_editable = (
        'location',
        'category',
        'pub_date',
        'is_published',
    )
    search_fields = (
        'title',
        'text',
        'location',
    )
    list_per_page = 10

    @staticmethod
    @admin.display(description='Текст')
    def text_short(obj: Post) -> str:
        """Укороченное описание поста для отображения в админке."""
        max_length = 150  # Максимальное количество символов для отображения
        if len(obj.text) > max_length:
            return obj.text[:max_length] + '...'
        else:
            return obj.text


class CategoryAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Category."""

    list_display = (
        'title',
        'description_short',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'slug',
    )
    list_filter = (
        'title',
        'description',
    )
    list_per_page = 10

    @staticmethod
    @admin.display(description='Описание')
    def description_short(obj: Category) -> str:
        """Укороченное названия категории для отображения в админке."""
        max_length = 50  # Максимальное количество символов для отображения
        if len(obj.description) > max_length:
            return obj.description[:max_length] + '...'
        else:
            return obj.description


class LocationAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Location."""

    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published',)
    list_filter = ('name',)
    list_per_page = 10


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
