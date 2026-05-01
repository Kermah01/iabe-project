from django.contrib import admin
from .models import Tombola, TombolaPrize, TombolaTicket


class TombolaPrizeInline(admin.TabularInline):
    model = TombolaPrize
    extra = 1


@admin.register(Tombola)
class TombolaAdmin(admin.ModelAdmin):
    list_display = ['title', 'ticket_price', 'status', 'start_date', 'draw_date', 'total_tickets_sold', 'is_active']
    list_filter = ['status', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TombolaPrizeInline]


@admin.register(TombolaTicket)
class TombolaTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'participant', 'tombola', 'is_paid', 'is_winner', 'prize_won', 'created_at']
    list_filter = ['is_paid', 'is_winner', 'tombola']
    search_fields = ['ticket_number', 'participant__username', 'participant__email']
    readonly_fields = ['ticket_number']
