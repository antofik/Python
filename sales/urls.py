from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import dancer_email_parser.views
import dressgallery.views
from djangoratings.views import AddRatingFromModel


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', dressgallery.views.home),
    url(r'^dress/(?P<id>\d{1,10})', dressgallery.views.dress_view),
    url(r'^dress/new$', dressgallery.views.dress_new),
    url(r'^dress/edit/(?P<id>\d{1,10})', dressgallery.views.dress_edit),
    url(r'^login/(?P<id>\d{1,10})', dressgallery.views.login),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rate-dress/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {'app_label': 'dressgallery', 'model': 'dress', 'field_name': 'rating',}),
    url(r'^remind_access_code/(?P<id>\d{1,10})', dressgallery.views.remind_access_code),
    url(r'^get_buyers/(?P<id>\d{1,10})', dressgallery.views.get_buyers),
    url(r'^send_notification', dressgallery.views.send_notification),
    url(r'^load_photo', dressgallery.views.load_photo),    
    url(r'^emailer', dressgallery.views.emailer),
    url(r'^emailing/register/(?P<email>.*)', dancer_email_parser.views.emailing),
    url(r'^emailing/click/(?P<email>.*)', dancer_email_parser.views.click),
    url(r'^smsing/register/(?P<phone>.*)/(?P<status>.*)', dancer_email_parser.views.smsing),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
