from cms.admin.pageadmin import PageAdmin
from cms.models import Page
from django.contrib.admin import *
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from filer.admin import FolderAdmin, FileAdmin, ClipboardAdmin, ImageAdmin
from filer.models import  Folder, File, Clipboard, Image


class AdminSiteEx(AdminSite):
    def __init__(self):
        super(AdminSiteEx, self).__init__()

    def app_index(self, request, app_label, extra_context=None):
        templateResponse = super(AdminSiteEx, self).app_index(request, app_label, extra_context)
        print dir(templateResponse)
        return templateResponse


site = AdminSiteEx()

site.register(Group, GroupAdmin)
site.register(User, UserAdmin)
site.register(Site, SiteAdmin)

site.register(Folder,FolderAdmin)
site.register(File,FileAdmin)
site.register(Clipboard, ClipboardAdmin)
site.register(Image, ImageAdmin)

site.register(Page, PageAdmin)
