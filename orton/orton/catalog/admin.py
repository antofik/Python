import admin_site as admin
from models import *
from tinymce.widgets import TinyMCE
import reversion

class CatalogAdmin(reversion.VersionAdmin):
    inlines = [] #required to some django or django cms bug with inlines.
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['purpose', 'action', 'usage']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(CatalogAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(CatalogItemModel, CatalogAdmin)


class CatalogCategoryAdmin(reversion.VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['description']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(CatalogCategoryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(CatalogCategoryModel, CatalogCategoryAdmin)


class CatalogVideoAdmin(reversion.VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['description']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(CatalogVideoAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(CatalogVideoModel, CatalogVideoAdmin)


class CatalogArticleAdmin(reversion.VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['description']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                ))
        return super(CatalogArticleAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, article, form, change):
        article.author = request.user
        article.save()
admin.site.register(CatalogArticleModel, CatalogArticleAdmin)


class CatalogNewsAdmin(reversion.VersionAdmin):
    date_hierarchy = 'date_added'
    fields = ("date_added", "name", "image", "short_description", "description")

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['description']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                ))
        return super(CatalogNewsAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, article, form, change):
        article.author = request.user
        article.save()
admin.site.register(CatalogNewsModel, CatalogNewsAdmin)


class CatalogAdviceAdmin(reversion.VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['description']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                ))
        return super(CatalogAdviceAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, article, form, change):
        article.author = request.user
        article.save()
admin.site.register(CatalogAdviceModel, CatalogAdviceAdmin)


class FeedbackAdmin(reversion.VersionAdmin):
    pass
admin.site.register(FeedbackModel, FeedbackAdmin)


class PartnerAdmin(reversion.VersionAdmin):
    pass
admin.site.register(PartnerModel, PartnerAdmin)


class DocumentAdmin(reversion.VersionAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['description']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(DocumentAdmin, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(DocumentModel, DocumentAdmin)


class CatalogCalendarAdmin(admin.StackedInline):
    model = CalendarModel
    exclude = ('m1','m10', 'm11', 'm12')
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12']:
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(CatalogCalendarAdmin, self).formfield_for_dbfield(db_field, **kwargs)
CatalogAdmin.inlines.append(CatalogCalendarAdmin)
admin.site.unregister(CatalogItemModel)
admin.site.register(CatalogItemModel, CatalogAdmin)
print 'inlines =', admin.ModelAdmin.inlines