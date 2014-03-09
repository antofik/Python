from django.conf.urls import *
from views import *

urlpatterns = patterns('catalog.views',
    url(r'^$', video_catalog),
    url(r'^video_item/(?P<id>\d+)', video_item),
)