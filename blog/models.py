from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField('Nom', max_length=100)
    slug = models.SlugField('Slug', unique=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('Titre', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='articles')
    excerpt = models.TextField('Extrait', max_length=500, blank=True)
    content = models.TextField('Contenu')
    image = models.ImageField('Image', upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField('Publié', default=False)
    published_at = models.DateTimeField('Date de publication', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
