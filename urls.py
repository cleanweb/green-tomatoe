from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
  
		('^$', 'views.index')  
    #('^pool/(?P<event_id>\d+)/$', 'reaktions.views.pool'),
)
