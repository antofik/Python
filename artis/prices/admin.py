from django.contrib import admin 
from models import *
    
class CategoryInline(admin.TabularInline):
    model = Item
    
    def __unicode__():
        return u'test'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','order',)
    search_fields = ('name',)
    ordering = ('order',)
    inlines = [CategoryInline,]    

class ItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'order', )
    search_fields = ('name',)
    ordering = ('category', 'order',)
    

admin.site.register(Category, CategoryAdmin) 
admin.site.register(Item, ItemAdmin) 
