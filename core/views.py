from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Partner, Testimonial, SiteSettings
from .forms import ContactForm
from programs.models import Program
from events.models import Event
from blog.models import Article


def get_settings():
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings.objects.create()
    return settings


def home(request):
    context = {
        'settings': get_settings(),
        'partners': Partner.objects.filter(is_active=True)[:6],
        'testimonials': Testimonial.objects.filter(is_active=True)[:4],
        'programs': Program.objects.filter(is_active=True)[:3],
        'upcoming_events': Event.objects.filter(is_active=True).order_by('start_date')[:3],
        'recent_articles': Article.objects.filter(is_published=True)[:3],
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'settings': get_settings(),
    }
    return render(request, 'core/about.html', context)


def partners(request):
    context = {
        'settings': get_settings(),
        'partners': Partner.objects.filter(is_active=True),
    }
    return render(request, 'core/partners.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a été envoyé avec succès !')
            return redirect('core:contact')
    else:
        form = ContactForm()
    context = {
        'settings': get_settings(),
        'form': form,
    }
    return render(request, 'core/contact.html', context)
