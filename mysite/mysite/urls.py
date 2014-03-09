from django.conf.urls import patterns, include, url
from mysite.views import *

urlpatterns = patterns('',
    (r'^$', repository_list),
    (r'^repository/(.*)', repository_details),
    (r'^userset/(.*)', userset_details),
    (r'^adduser', adduser),
    (r'^createuser', createuser),
    (r'^createuserset', create_user_details),
    (r'^createrepository', create_repository),
    (r'^deleterepository/(.*)', delete_repository),
)
