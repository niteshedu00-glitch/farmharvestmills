from django.contrib import admin
from django.utils.html import format_html
from .models import Enquiry, NewsletterSubscriber


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'enquiry_type', 'status_badge', 'created_at')
    list_filter = ('enquiry_type', 'status', 'created_at')
    search_fields = ('name', 'phone', 'email', 'company_name', 'message')
    list_editable = ()
    readonly_fields = ('name', 'phone', 'email', 'company_name', 'enquiry_type', 'message', 'created_at')
    fieldsets = (
        ('Customer Details', {'fields': ('name', 'phone', 'email', 'company_name', 'created_at')}),
        ('Enquiry', {'fields': ('enquiry_type', 'message')}),
        ('Manage', {'fields': ('status', 'admin_notes')}),
    )
    date_hierarchy = 'created_at'

    def status_badge(self, obj):
        colors = {'new': '#dc2626', 'in_progress': '#f59e0b', 'closed': '#16a34a'}
        return format_html(
            '<b style="color:{}">{}</b>', colors.get(obj.status, '#333'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def has_add_permission(self, request):
        # Enquiries come from the public website form, not created in admin.
        return False


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
