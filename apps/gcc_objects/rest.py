#!/usr/bin/env python

from restive import Service

from models import Object
from gcc_projects.models import Project

from gcc_editor import rest

service = Service()

@service.add
def new(request, pid):
    return rest.new(request, pid, 'Object', Object, solid=True, persistent=False, type='image')

urlpatterns = service.urls()

# vim: et sw=4 sts=4
