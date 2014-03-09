# coding=utf-8
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class CatalogAppHook(CMSApp):
    name = _(u"Каталог")
    urls = ["catalog.urls"]
apphook_pool.register(CatalogAppHook)


class CatalogPreviewAppHook(CMSApp):
    name = _(u"Превью каталога")
    urls = ["catalog.urls_preview"]
apphook_pool.register(CatalogPreviewAppHook)


class CatalogVideoAppHook(CMSApp):
    name = _(u"Видеоматериалы")
    urls = ["catalog.urls_video"]
apphook_pool.register(CatalogVideoAppHook)


class CatalogArticlesAppHook(CMSApp):
    name = _(u"Статьи")
    urls = ["catalog.urls_articles"]
apphook_pool.register(CatalogArticlesAppHook)


class CatalogNewsAppHook(CMSApp):
    name = _(u"Новости")
    urls = ["catalog.urls_news"]
apphook_pool.register(CatalogNewsAppHook)


class CatalogAdvicesAppHook(CMSApp):
    name = _(u"Советы")
    urls = ["catalog.urls_advices"]
apphook_pool.register(CatalogAdvicesAppHook)
