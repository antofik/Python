# coding=utf-8
try:
    from cms.plugin_base import CMSPluginBase
    from cms.plugin_pool import plugin_pool
    from django.utils.translation import ugettext_lazy as _
    from models import CatalogItemModel, CatalogNewsModel, CatalogArticleModel, CatalogAdviceModel, CatalogCategoryModel, PartnerModel, DocumentModel

    class LastNewsPlugin(CMSPluginBase):
        name = _(u"Последняя новость")
        render_template = "plugins/catalog/last-news.html"

        def render(self, context, instance, placeholder):
            items = CatalogNewsModel.objects.all()[:1]
            item = items[0] if items else None
            context.update({'instance':instance, 'item':item})
            return context

    plugin_pool.register_plugin(LastNewsPlugin)


    class LastArticlePlugin(CMSPluginBase):
        name = _(u"Последняя статья")
        render_template = "plugins/catalog/last-article.html"

        def render(self, context, instance, placeholder):
            items = CatalogArticleModel.objects.all()[:1]
            item = items[0] if items else None
            context.update({'instance':instance, 'item':item})
            return context

    plugin_pool.register_plugin(LastArticlePlugin)


    class LastAdvicesPlugin(CMSPluginBase):
        name = _(u"Последние советы")
        render_template = "plugins/catalog/last-advices.html"

        def render(self, context, instance, placeholder):
            items = CatalogAdviceModel.objects.all()[:1]
            item = items[0] if items else None
            context.update({'instance':instance, 'item':item})
            return context

    plugin_pool.register_plugin(LastAdvicesPlugin)


    class FeedbackPlugin(CMSPluginBase):
        name = _(u"Форма обратной связи")
        render_template = "plugins/feedback.html"

        def render(self, context, instance, placeholder):
            return context

    plugin_pool.register_plugin(FeedbackPlugin)


    class CatalogNavigatorPlugin(CMSPluginBase):
        name = _(u"Путеводитель по каталогу")
        render_template = "plugins/catalog/catalog-navigator.html"

        def render(self, context, instance, placeholder):
            categories = []
            all = CatalogCategoryModel.objects.select_related('parent').all()
            for category in all:
                if not category.parent:
                    category.subcategories = []
                    categories.append(category)
            for category in categories:
                for sub in all:
                    if not sub.parent:
                        continue
                    if sub.parent.name==category.name:
                        category.subcategories.append(sub)
            context.update({'categories':categories})
            return context

    plugin_pool.register_plugin(CatalogNavigatorPlugin)


    class CatalogPartnersPlugin(CMSPluginBase):
        name = _(u"Партнёры")
        render_template = "plugins/catalog/partners.html"

        def render(self, context, instance, placeholder):
            all = PartnerModel.objects.all()
            context.update({'partners':all})
            return context

    plugin_pool.register_plugin(CatalogPartnersPlugin)


    class CatalogDocumentsPlugin(CMSPluginBase):
        name = _(u"Документы")
        render_template = "plugins/catalog/documents.html"

        def render(self, context, instance, placeholder):
            all = DocumentModel.objects.all()
            context.update({'items':all})
            return context

    plugin_pool.register_plugin(CatalogDocumentsPlugin)


    class CatalogCalendarPlugin(CMSPluginBase):
        name = _(u"Календарь")
        render_template = "plugins/catalog/calendar.html"

        def render(self, context, instance, placeholder):
            all = filter(lambda x: x.calendar is not None, list(CatalogItemModel.objects.select_related("calendar", "category", "category.parent").all()))
            for item in all:
                c = item.calendar
                if not c:
                    all.remove(item)
                    continue
                has_calendar = c.m2 or c.m3 or c.m4 or c.m5 or c.m6 or c.m7 or c.m8 or c.m9
                if not has_calendar:
                    all.remove(item)
                    continue
            context.update({'items':all, 'monthes': range(1,9)})
            return context

    plugin_pool.register_plugin(CatalogCalendarPlugin)

except Exception,e :
    print 'Error: ', unicode(e)