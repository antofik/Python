from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import main.views


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', main.views.home),
    url(r'^algo/(?P<algo_id>[^/]+)/(?P<language_code>[^/]*)$', main.views.standard_algorithm),
    url(r'^fork/(?P<algo_id>[^/]+)$', main.views.user_algorithm),
    url(r'^fork/(?P<algo_id>[^/]+)/(?P<language_code>[^/]+)$', main.views.user_algorithm),
    url(r'^merge$', main.views.merge_algorithm),
    url(r'^request_merge$', main.views.request_merge),
    url(r'^request_become_standard$', main.views.request_become_standard),
    url(r'^create$', main.views.create_algorithm),
    url(r'^create/(?P<language_id>[^/]*)$', main.views.create_algorithm_with_language),
    url(r'^implement/(?P<algo_id>[^/]*)$', main.views.implement_algorithm),
    url(r'^implement/(?P<algo_id>[^/]+)/(?P<language_id>[^/]*)$', main.views.implement_algorithm_with_language),
    url(r'^save$', main.views.save_algorithm),
    url(r'^fork$', main.views.fork_algorithm),
    url(r'^face$', main.views.face_recognition),
    url(r'^recognize_face', main.views.recognize_face),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
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
