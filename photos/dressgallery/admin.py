﻿from django.contrib import admin 
from models import *

def dress_block(modeladmin, request, queryset):
    queryset.update(blocked=True)
dress_block.short_description = u'Заблокировать объявления'

def dress_unblock(modeladmin, request, queryset):
    queryset.update(blocked=False)
dress_unblock.short_description = u'Разблокировать объявления'
    
class PhotoInline(admin.TabularInline):
    model = Photo

class PhotoAdmin(admin.ModelAdmin):
    pass

class DressAdmin(admin.ModelAdmin):
    inlines = [PhotoInline,]    
    pass
    
admin.site.register(Photo, PhotoAdmin) 
admin.site.register(Tournament, DressAdmin)
