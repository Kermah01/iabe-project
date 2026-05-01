from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Program, ProgramRegistration
from .forms import ProgramRegistrationForm


def program_list(request):
    programs = Program.objects.filter(is_active=True)
    destination = request.GET.get('destination')
    program_type = request.GET.get('type')
    if destination:
        programs = programs.filter(destination=destination)
    if program_type:
        programs = programs.filter(program_type=program_type)
    context = {
        'programs': programs,
        'destinations': Program.DESTINATIONS,
        'program_types': Program.PROGRAM_TYPES,
        'current_destination': destination,
        'current_type': program_type,
    }
    return render(request, 'programs/list.html', context)


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug, is_active=True)
    already_registered = False
    if request.user.is_authenticated:
        already_registered = ProgramRegistration.objects.filter(
            program=program, member=request.user
        ).exists()
    context = {
        'program': program,
        'already_registered': already_registered,
    }
    return render(request, 'programs/detail.html', context)


@login_required
def program_register(request, slug):
    program = get_object_or_404(Program, slug=slug, is_active=True)
    if ProgramRegistration.objects.filter(program=program, member=request.user).exists():
        messages.warning(request, 'Vous êtes déjà inscrit à ce programme.')
        return redirect('programs:detail', slug=slug)
    if program.spots_left <= 0:
        messages.error(request, 'Désolé, ce programme est complet.')
        return redirect('programs:detail', slug=slug)
    if request.method == 'POST':
        form = ProgramRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.program = program
            registration.member = request.user
            registration.amount_paid = program.cost
            registration.save()
            messages.success(request, f'Inscription au programme "{program.title}" effectuée !')
            return redirect('members:dashboard')
    else:
        form = ProgramRegistrationForm()
    return render(request, 'programs/register.html', {'program': program, 'form': form})
