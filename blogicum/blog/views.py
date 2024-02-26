from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def index(request: HttpRequest) -> HttpResponse:
    """Представление главной страницы блога.

    Посты должны быть расположены в обратном порядке по номеру публикации.
    """
    post_list: list[Post] = Post.objects.filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Представление станицы поста."""
    post: Post = get_object_or_404(
        Post.objects.filter(
            pub_date__lte=datetime.now(),
            is_published=True,
            pk=post_id,
            category__is_published=True),
        id=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Представление страницы категории постов."""
    category: Category = get_object_or_404(
        Category.objects.values('title', 'description').filter(
            is_published=True),
        slug=category_slug
    )
    post_list: Post = Post.objects.filter(
        category__slug=category_slug,
        pub_date__lte=datetime.now(),
        is_published=True
    )
    context: dict[str, Category | list[Post]] = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Представление страницы 404 ошибки."""
    return render(request, 'blog/404.html', status=404)
