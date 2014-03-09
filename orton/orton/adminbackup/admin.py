# coding=utf-8
from django.contrib.admin import ModelAdmin
import admin_site
from adminbackup.models import Backup


class BackupAdmin(ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_urls(self):
        patterns = super(BackupAdmin, self).get_urls()
        from urls import urlpatterns
        return urlpatterns + patterns


admin_site.site.register(Backup, BackupAdmin)


