#!/usr/bin/env python
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^ajax/projects/', include('gcc_projects.rest')),
    (r'^ajax/sprites/', include('gcc_sprites.rest')),
    (r'^ajax/objects/', include('gcc_objects.rest')),
    (r'^ajax/maps/', include('gcc_maps.rest')),
    (r'^ajax/media/', include('gcc_media.rest')),
)

# vim: et sw=4 sts=4
