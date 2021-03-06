from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import Group, UserAdmin, GroupAdmin
from django.utils.safestring import mark_safe

from admin_interface.admin import Theme, ThemeAdmin

from .models import CoreUser, Inquiry


class CoreAdminSite(admin.AdminSite):
    """A subclass of the default AdminSite

    Django docs:
    https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#adminsite-objects
    """
    site_header = f'{settings.SITE_NAME} Admin Panel'
    site_title = f'{settings.SITE_NAME} Admin Panel'


core_admin_site = CoreAdminSite()


@admin.register(CoreUser, site=core_admin_site)
class CoreUserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field.

    You can find detailed examples here:
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#a-full-example
    https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username#Register%20your%20new%20User%20model%20with%20Django%20admin
    """

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Inquiry, site=core_admin_site)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'submission_date')
    fields = ('name', 'email', 'submission_date', 'message', 'ip_link', 'notes')
    readonly_fields = ('name', 'email', 'submission_date', 'message', 'ip_link')

    def ip_link(self, instance):
        ip = instance.ip_address
        return mark_safe(f'<a href="https://www.abuseipdb.com/check/{ip}" rel="noreferrer" target="_blank">{ip}</a>')
    ip_link.short_description = 'IP address'

    def has_add_permission(self, request):
        return False


core_admin_site.register(Group, GroupAdmin)
core_admin_site.register(Theme, ThemeAdmin)
