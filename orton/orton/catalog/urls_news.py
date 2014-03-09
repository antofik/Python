from django.conf.urls import *
from views import *

urlpatterns = patterns('catalog.views',
    url(r'^$', news_list),
    url(r'^news_item/(?P<id>\d+)', news_item),
)