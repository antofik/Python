from django.conf.urls import patterns, url
from django.conf import settings
from polls import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test/?$', views.test),
    url(r'^test/thanks/?$', views.thanks),
    url(r'^test/results/(?P<id>\d+)/$', views.results),
    url(r'^test/(?P<id>\d+)/$', views.detail),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)