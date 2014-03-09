from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from svnadmin.views import hello
#import views

#admin.autodiscover()

urlpatterns = patterns('',
    
 #    url(r'^', include('cms.urls')),
     url(r'^', include(hello)),
     
 #    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
 #    url(r'^admin/', include(admin.site.urls)),
)
