from django.conf.urls import *
from views import *

urlpatterns = patterns('catalog.views',
    url(r'^$', image_category),
    #url(r'^category/(?P<name>[^/]*)', category),
    url(r'^image_category/(?P<name>[^/]*)', image_category),
    #url(r'^item/(?P<name>[^/]*)', item),
)