from django.contrib import admin
from .models import Partner, Testimonial, ContactMessage, SiteSettings


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'country', 'is_active']
    list_filter = ['partner_type', 'country', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'content']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Général', {'fields': ('site_name', 'tagline', 'hero_image')}),
        ('À propos', {'fields': ('about_text', 'mission', 'vision', 'objectives')}),
        ('Contact', {'fields': ('address', 'phone', 'email')}),
        ('Réseaux sociaux', {'fields': ('facebook_url', 'instagram_url', 'tiktok_url')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
