from django.conf.urls.defaults import *

from django.conf import settings
from django.shortcuts import redirect
import admin_site
from catalog import views

#admin.autodiscover()

admin_site.autodiscover()

urlpatterns = patterns('',
    #(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin_site.site.urls)),
    (r'^feedback', views.feedback),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^settings/', include('dbsettings.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('cms.urls')),
#    url(r'.*', lambda request: redirect('/')),
)

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^backups/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BACKUP_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns