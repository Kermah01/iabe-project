from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member, MembershipPayment, MemberDocument


@admin.register(Member)
class MemberAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'member_type',
                    'is_membership_active', 'date_joined']
    list_filter = ['member_type', 'is_membership_active', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'organization_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Informations IABE', {
            'fields': ('member_type', 'phone', 'city', 'country', 'organization_name',
                       'bio', 'photo', 'is_membership_active', 'membership_paid_until',
                       'date_joined_association')
        }),
    )


@admin.register(MembershipPayment)
class MembershipPaymentAdmin(admin.ModelAdmin):
    list_display = ['member', 'payment_type', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['payment_type', 'payment_method', 'status']
    search_fields = ['member__username', 'member__email', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MemberDocument)
class MemberDocumentAdmin(admin.ModelAdmin):
    list_display = ['member', 'title', 'uploaded_at']
    search_fields = ['member__username', 'title']
