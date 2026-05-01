from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberRegistrationForm, MemberLoginForm, MemberProfileForm, MembershipPaymentForm
from .models import MembershipPayment, MemberDocument


def register(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Bienvenue ! Votre compte a été créé avec succès.')
            return redirect('members:dashboard')
    else:
        form = MemberRegistrationForm()
    return render(request, 'members/register.html', {'form': form})


def member_login(request):
    if request.method == 'POST':
        form = MemberLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenue, {user.get_full_name() or user.username} !')
            return redirect('members:dashboard')
    else:
        form = MemberLoginForm()
    return render(request, 'members/login.html', {'form': form})


def member_logout(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('core:home')


@login_required
def dashboard(request):
    payments = MembershipPayment.objects.filter(member=request.user)[:10]
    documents = MemberDocument.objects.filter(member=request.user)
    context = {
        'payments': payments,
        'documents': documents,
    }
    return render(request, 'members/dashboard.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('members:profile')
    else:
        form = MemberProfileForm(instance=request.user)
    return render(request, 'members/profile.html', {'form': form})


@login_required
def membership_payment(request):
    PRICES = {
        'adhesion': 30000,
        'annual': 100000,
    }
    if request.method == 'POST':
        form = MembershipPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.member = request.user
            payment.amount = PRICES.get(payment.payment_type, 0)
            payment.status = 'pending'
            payment.save()
            messages.success(request, f'Paiement de {payment.amount} FCFA initié. Vous recevrez une confirmation.')
            return redirect('members:dashboard')
    else:
        form = MembershipPaymentForm()
    return render(request, 'members/payment.html', {'form': form, 'prices': PRICES})


@login_required
def payment_history(request):
    payments = MembershipPayment.objects.filter(member=request.user)
    return render(request, 'members/payment_history.html', {'payments': payments})
