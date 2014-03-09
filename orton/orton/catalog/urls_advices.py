from django.conf.urls import *
from views import *

urlpatterns = patterns('catalog.views',
    url(r'^$', advices_list),
    url(r'^advices_item/(?P<id>\d+)', advices_item),
)