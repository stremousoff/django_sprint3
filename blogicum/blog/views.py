from http import HTTPStatus

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import NUMBER_OF_POSTS
from .models import Category, Post


def filter_posts(obj: Post.objects) -> QuerySet[Post]:
    """Получение постов из базы данных.

    Возвращает:
    QuerySet[Post]: объект QuerySet содержащий список постов

    Пост должен быть:
    - дата публиции не позднее текущего момента;
    - разрешение на публикацию;
    - категория поста должна иметь разрешение на публикацию;
    """
    return obj.select_related(
        'category', 'location', 'author').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request: HttpRequest) -> HttpResponse:
    """Представление главной страницы блога.

    Параметры:
    request (HttpRequest): объект запроса

    Возвращает:
    HttpResponse: объект ответа

    Посты должны быть:
    - дата публиции не позднее текущего момента;
    - разрешение на публикацию;
    - категория поста должна иметь разрешение на публикацию;
    - расположены в обратном порядке по дате публикации;
    - последние пять постов.
    """
    post_list: QuerySet[Post] = filter_posts(Post.objects)[:NUMBER_OF_POSTS]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """Представление станицы поста.

    Параметры:
    request (HttpRequest): объект запроса
    post_id (int): идентификатор поста

    Возвращает:
    HttpResponse: объект ответа

    Пост должен быть:
    - дата публиции не позднее текущего момента;
    - разрешение на публикацию;
    - категория поста должна иметь разрешение на публикацию;
    - если пост не найден, должна вернуться ошибка 404.
    """
    post: Post = get_object_or_404(filter_posts(Post.objects), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Представление страницы категории постов.

    Параметры:
    request (HttpRequest): объект запроса
    category_slug (str): идентификатор категории

    Возвращает:
    HttpResponse: объект ответа

    Категория должна быть:
    - иметь разрешение на публикацию.
    Список постов должен быть:
    - категория поста имеет разрешение на публикацию;
    - дата публиции не позднее текущего момента;
    - разрешение на публикацию.
    """
    category: Category = get_object_or_404(
        Category, is_published=True, slug=category_slug
    )
    post_list: QuerySet[Post] = filter_posts(category.posts)
    context: dict[str, Category | QuerySet[Post]] = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Представление страницы 404 ошибки.

    Параметры:
    request (HttpRequest): объект запроса
    exception (Exception): исключение

    Возвращает:
    HttpResponse: объект ответа
    """
    return render(request, 'blog/404.html', status=HTTPStatus.NOT_FOUND)
