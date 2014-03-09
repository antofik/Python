from django.conf.urls import *
from views import *

urlpatterns = patterns('catalog.views',
    url(r'^$', articles_list),
    url(r'^articles_item/(?P<id>\d+)', articles_item),
)