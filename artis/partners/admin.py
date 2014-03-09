from django.contrib import admin 
from models import *

class CategoryInline(admin.TabularInline):
    model = Item
    
    def __unicode__():
        return u'test'

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'text', 'image')
    search_fields = ('title', 'text')
    ordering = ('added', 'title')
    

admin.site.register(Item, ItemAdmin) 
