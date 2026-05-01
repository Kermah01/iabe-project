from django.shortcuts import render, get_object_or_404
from .models import Article, Category


def article_list(request):
    articles = Article.objects.filter(is_published=True)
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    categories = Category.objects.all()
    context = {
        'articles': articles,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'blog/list.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related_articles = Article.objects.filter(
        is_published=True, category=article.category
    ).exclude(pk=article.pk)[:3]
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'blog/detail.html', context)
