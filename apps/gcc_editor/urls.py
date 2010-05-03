#!/usr/bin/env python
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import views

urlpatterns = patterns('',
    (r'^$', views.index),
)

# vim: et sw=4 sts=4
