from django.conf.urls.defaults import *

urlpatterns = patterns('datafeed.views',
    url('^$', 'spit_columns', name='datafeed'),
    url('post/', 'post', name='datafeed_post'), 
)
