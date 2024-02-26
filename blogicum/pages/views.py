from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def about(request: HttpRequest) -> HttpResponse:
    """Представление страницы о сайте."""
    return render(request, 'pages/about.html')


def rules(request: HttpRequest) -> HttpResponse:
    """Представление страницы правил."""
    return render(request, 'pages/rules.html')
