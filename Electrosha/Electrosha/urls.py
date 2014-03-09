from django.conf.urls import patterns, include, url
from django.contrib import admin
import webparser.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'webparser.views.index', name='index'),
    # url(r'^Electrosha/', include('Electrosha.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
