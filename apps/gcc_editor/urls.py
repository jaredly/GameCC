#!/usr/bin/env python
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^ajax/project/', include('gcc_projects.rest')),
    (r'^ajax/sprite/', include('gcc_sprites.rest')),
    (r'^ajax/object/', include('gcc_objects.rest')),
    (r'^ajax/map/', include('gcc_maps.rest')),
    (r'^ajax/media/', include('gcc_media.rest')),
    (r'^upload/(?P<ftype>[^/]+)/$', 'gcc_media.views.upload')
)

# vim: et sw=4 sts=4
