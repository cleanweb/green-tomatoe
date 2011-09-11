from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url('^$', 'views.index', name='index'),
    url('^datafeed/', include('datafeed.urls')),
)
