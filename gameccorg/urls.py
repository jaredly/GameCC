from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import serve_media
import views

urlpatterns = patterns('',
    (r'^$', views.home),
    (r'^browse/(?:(?P<category>.+)/)?$', views.browse),
    (r'^categories/$', views.categories),

    (r'^blog/', include('basic.blog.urls')),
    # Example:
    # (r'^gameccorg/', include('gameccorg.foo.urls')),

    (r'^media/(?P<path>.*)$', serve_media.serve_all, {'document_root' : settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
