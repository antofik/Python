from cms.admin.pageadmin import PageAdmin
from django.contrib import admin
from models import CMSRedirect
from cms.models.pagemodel import Page

class CMSRedirectAdmin(admin.TabularInline):
    model = CMSRedirect
    fk_name="page_from"
    extra=1

PageAdmin.inlines.append(CMSRedirectAdmin)

admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)
