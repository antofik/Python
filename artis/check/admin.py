from django.contrib import admin 
from models import *

class CategoryInline(admin.TabularInline):
    model = Item
    
    def __unicode__(self):
        return self.title

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'text', 'code', 'added', 'date_ready')
    search_fields = ('title', 'code')
    ordering = ('added', 'title', 'date_ready')
    

admin.site.register(Item, ItemAdmin) 
