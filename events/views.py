from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, EventRegistration


def event_list(request):
    events = Event.objects.filter(is_active=True)
    event_type = request.GET.get('type')
    if event_type:
        events = events.filter(event_type=event_type)
    context = {
        'events': events,
        'event_types': Event.EVENT_TYPES,
        'current_type': event_type,
    }
    return render(request, 'events/list.html', context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    already_registered = False
    if request.user.is_authenticated:
        already_registered = EventRegistration.objects.filter(
            event=event, member=request.user
        ).exists()
    context = {
        'event': event,
        'already_registered': already_registered,
    }
    return render(request, 'events/detail.html', context)


@login_required
def event_register(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    if EventRegistration.objects.filter(event=event, member=request.user).exists():
        messages.warning(request, 'Vous êtes déjà inscrit à cet événement.')
        return redirect('events:detail', slug=slug)
    if event.spots_left <= 0:
        messages.error(request, 'Désolé, cet événement est complet.')
        return redirect('events:detail', slug=slug)
    EventRegistration.objects.create(event=event, member=request.user, status='confirmed')
    messages.success(request, f'Inscription à "{event.title}" confirmée !')
    return redirect('members:dashboard')
