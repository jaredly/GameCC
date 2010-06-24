#!/usr/bin/env python

import inspect

from models import Project

from restive import Service

from gcc_sprites.models import Sprite
from gcc_objects.models import Object
from gcc_maps.models import Map
from django.contrib.auth.models import AnonymousUser

service = Service()

@service.add
def load(request, project):
    if isinstance(request.user, AnonymousUser):
        return {'error':'not logged in', 'action':'/accounts/login/?next=/editor/#%s' % project}
    obj = Project.objects.get(author=request.user, slug=project)
    res = {'title': obj.title} # expose Project metadata through a different call -- get the form.
    sprites = obj.asset_sprites.all()
    res['_models'] = {'project':obj}
    res['_models']['assets'] = {
            'sprites': obj.asset_sprites.all(),
            'objects': obj.asset_objects.all(),
            'maps': obj.asset_maps.all()
        }
    res['_models'] = [obj] + list(obj.asset_sprites.all()) + \
            list(obj.asset_objects.all()) + \
            list(obj.asset_maps.all())
    return res

@service.add(name = 'folder/blank')
def blank(request):
    return []

@service.add(name = '(?P<pid>\d+)/folder/(?P<atype>\w+)s')
def folder(request, pid, atype):
    proj = Project.objects.get(pk = int(pid))
    if atype not in ['sprite', 'object', 'map']:
        raise Exception,'invalid asset type'
    model = {'sprite':Sprite, 'object':Object, 'map':Map}[atype]
    data = proj.load_folder(atype)
    res = []
    ext_ize(data, res, model)
    return res

def ext_ize(raw, dest, model):
    for item in raw:
        if type(item) == int:
            dest.append({'id':item, 'text':model.objects.get(pk=item).title, 'leaf':True})
        else:
            children = []
            dest.append({'text':item[0], 'children':children})
            ext_ize(children, item[1], model)

urlpatterns = service.urls()

# vim: et sw=4 sts=4
