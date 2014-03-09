from django.contrib import admin 
from models import *
from tinymce.widgets import TinyMCE
from django.core.urlresolvers import reverse

class CategoryInline(admin.TabularInline):
    model = Item
    
    def __unicode__():
        return u'test'

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'image')
    search_fields = ('title', 'text')
    ordering = ('added', 'title')
    fields = ('order', 'title', 'text', 'image',)
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['text', 'excerpt']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
               # mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(ItemAdmin, self).formfield_for_dbfield(db_field, **kwargs)    
    

admin.site.register(Item, ItemAdmin) 
