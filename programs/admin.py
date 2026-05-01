from django.contrib import admin
from .models import Program, ProgramRegistration


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'program_type', 'destination', 'duration', 'cost', 'start_date', 'max_participants', 'is_active']
    list_filter = ['program_type', 'destination', 'is_active']
    search_fields = ['title', 'description', 'partner_institution']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProgramRegistration)
class ProgramRegistrationAdmin(admin.ModelAdmin):
    list_display = ['member', 'program', 'status', 'amount_paid', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['member__username', 'member__email', 'program__title']
