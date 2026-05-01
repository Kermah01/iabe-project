from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'location', 'start_date', 'max_participants', 'is_active']
    list_filter = ['event_type', 'is_active']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['member', 'event', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['member__username', 'member__email', 'event__title']
