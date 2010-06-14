#!/usr/bin/env python

from restive import Service

from models import Sprite
from gcc_projects.models import Project

from gcc_editor import rest

service = Service()

@service.add
def new(request, pid):
    return rest.new(request, pid, 'Sprite', Sprite, speed=1, collision_type=1, collision_attrs="")

urlpatterns = service.urls()

# vim: et sw=4 sts=4
