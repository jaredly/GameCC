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
    (r'^create/$', views.create),
    (r'^create/project/$', views.new_project),

    (r'^editor/', include('gcc_editor.urls')),

    (r'^blog/', include('basic.blog.urls')),

    (r'^media/(?P<path>.*)$', serve_media.serve_all, {'document_root' : settings.MEDIA_ROOT}),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

