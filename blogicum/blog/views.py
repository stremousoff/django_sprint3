from django.shortcuts import get_object_or_404, render

from .constants import NUMBER_OF_POSTS
from .models import Category, Post


def index(request):
    """Представление главной страницы блога."""
    post_list = Post.objects.published()[:NUMBER_OF_POSTS]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    """Представление станицы поста."""
    post = get_object_or_404(Post.objects.published(), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Представление страницы категории постов."""
    category = get_object_or_404(
        Category, is_published=True, slug=category_slug
    )
    post_list = category.posts.published()
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
