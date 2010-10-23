from django.conf.urls.defaults import *

urlpatterns = patterns('thumbnailer.views',

    (r'thumb/(?P<path>.*)', 'produce_thumbnail_and_redirect'),

)