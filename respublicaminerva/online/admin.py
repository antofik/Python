from django.contrib import admin
from models import *

class EntryTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(EntryType, EntryTypeAdmin)

class MeasureTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(MeasureType, MeasureTypeAdmin)
