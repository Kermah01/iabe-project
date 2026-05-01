import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Tombola, TombolaTicket, TombolaPrize
from .forms import TombolaTicketForm


def tombola_list(request):
    tombolas = Tombola.objects.filter(is_active=True)
    context = {'tombolas': tombolas}
    return render(request, 'tombola/list.html', context)


def tombola_detail(request, slug):
    tombola = get_object_or_404(Tombola, slug=slug, is_active=True)
    prizes = tombola.prizes.all()
    my_tickets = []
    if request.user.is_authenticated:
        my_tickets = TombolaTicket.objects.filter(tombola=tombola, participant=request.user)
    winners = TombolaTicket.objects.filter(tombola=tombola, is_winner=True).select_related('prize_won', 'participant')
    context = {
        'tombola': tombola,
        'prizes': prizes,
        'my_tickets': my_tickets,
        'winners': winners,
    }
    return render(request, 'tombola/detail.html', context)


@login_required
def tombola_buy_ticket(request, slug):
    tombola = get_object_or_404(Tombola, slug=slug, is_active=True, status='active')
    if request.method == 'POST':
        form = TombolaTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.tombola = tombola
            ticket.participant = request.user
            ticket.is_paid = True
            ticket.save()
            messages.success(request, f'Ticket #{ticket.ticket_number} acheté avec succès ! Bonne chance !')
            return redirect('tombola:detail', slug=slug)
    else:
        form = TombolaTicketForm()
    context = {
        'tombola': tombola,
        'form': form,
    }
    return render(request, 'tombola/buy_ticket.html', context)


def tombola_winners(request, slug):
    tombola = get_object_or_404(Tombola, slug=slug)
    winners = TombolaTicket.objects.filter(
        tombola=tombola, is_winner=True
    ).select_related('prize_won', 'participant').order_by('prize_won__rank')
    context = {
        'tombola': tombola,
        'winners': winners,
    }
    return render(request, 'tombola/winners.html', context)


@staff_member_required
def tombola_draw(request, slug):
    tombola = get_object_or_404(Tombola, slug=slug)
    if request.method == 'POST':
        prizes = tombola.prizes.all()
        paid_tickets = list(TombolaTicket.objects.filter(tombola=tombola, is_paid=True, is_winner=False))
        if not paid_tickets:
            messages.error(request, 'Aucun ticket payé disponible pour le tirage.')
            return redirect('tombola:detail', slug=slug)
        for prize in prizes:
            if paid_tickets:
                winner_ticket = random.choice(paid_tickets)
                winner_ticket.is_winner = True
                winner_ticket.prize_won = prize
                winner_ticket.save()
                paid_tickets.remove(winner_ticket)
        tombola.status = 'completed'
        tombola.save()
        messages.success(request, 'Tirage au sort effectué avec succès !')
        return redirect('tombola:winners', slug=slug)
    context = {'tombola': tombola}
    return render(request, 'tombola/draw.html', context)
