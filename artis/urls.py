from django.conf.urls import patterns, include, url
from views import *
from prices.views import pricelist
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
import auth.views
import online.views
from news.views import newslist
from partners.views import partnerslist
from check.views import checkform, check_postmessage, check_postorder

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', home),
    (r'^check$', checkform),
    (r'^check/message$', check_postmessage),
    (r'^check/order$', check_postorder),
    (r'^online$', online.views.online),
    (r'^online/entries/(\d{4})-(\d{1,2})-(\d{1,2})$', online.views.entry_list),
    (r'^online/measures', online.views.measures),
    (r'^news$', newslist),
    (r'^partners$', partnerslist),
    (r'^contact$', contact),
    (r'^prices$', pricelist),
    (r'^shop$', shop),
    (r'^about$', about),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/profile', auth.views.profile),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^login', ajax_login),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
