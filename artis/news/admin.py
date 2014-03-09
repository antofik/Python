from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from testtinymce.testapp.admin import TinyMCEFlatPageAdmin
from models import *
from tinymce.widgets import TinyMCE
from django.core.urlresolvers import reverse

class CategoryInline(admin.TabularInline):
    model = Item
    
    def __unicode__(self):
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
            ))
        return super(ItemAdmin, self).formfield_for_dbfield(db_field, **kwargs)    
    

admin.site.register(Item, ItemAdmin)



admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)