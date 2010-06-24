#!/usr/bin/env python

from restive import Service

from models import Sprite
from gcc_projects.models import Project

from gcc_editor import rest

service = Service()

@service.add
def new(request, pid):
    return rest.new(request, pid, 'Sprite', Sprite, speed=1, collision_type=1, collision_attrs="")

@service.add(name = '(?P<id>\d+)/save_subimages')
def save_subimages(request, id, subimages):
    obj = Sprite.objects.get(pk=id)
    obj.subimages = str(subimages)
    obj.save()
    return {}

urlpatterns = service.urls()

# vim: et sw=4 sts=4
