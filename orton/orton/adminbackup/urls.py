from django.conf.urls import *
from views import *

urlpatterns = patterns('',
    url(r'^$', backup),
    url(r'^create/$', create),
    url(r'^restore/(.+)/$', restore),
    url(r'^delete/(.+)/$', delete),
)