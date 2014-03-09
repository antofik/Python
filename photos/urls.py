from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import dressgallery.views
from djangoratings.views import AddRatingFromModel


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', dressgallery.views.home),
    url(r'^dress/(?P<id>\d{1,10})', dressgallery.views.dress_view),
    url(r'^dress/new$', dressgallery.views.dress_new),
    url(r'^dress/edit/(?P<id>\d{1,10})', dressgallery.views.dress_edit),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^load_photo', dressgallery.views.load_photo),

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
