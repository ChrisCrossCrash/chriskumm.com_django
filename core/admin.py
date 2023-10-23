from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import Group, GroupAdmin
from django_modern_user.admin import ModernUserAdmin

from admin_interface.admin import Theme, ThemeAdmin

from .models import CoreUser


class CoreAdminSite(admin.AdminSite):
    """A subclass of the default AdminSite

    Django docs:
    https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#adminsite-objects
    """

    site_header = f"{settings.SITE_NAME} Admin Panel"
    site_title = f"{settings.SITE_NAME} Admin Panel"


core_admin_site = CoreAdminSite()


@admin.register(CoreUser)
class CoreUserAdmin(ModernUserAdmin):
    pass


core_admin_site.register(Group, GroupAdmin)
core_admin_site.register(Theme, ThemeAdmin)
