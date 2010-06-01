#!/usr/bin/env python

import inspect

from models import Project

from restive import Service

service = Service()

@service.add
def load(request, project):
    # return {'proj':project}
    obj = Project.objects.get(author=request.user, slug=project)
    res = {'title': obj.title} # expose Project metadata through a different call -- get the form.
    sprites = obj.asset_sprites.order_by('order')
    res['_models'] = {'project':obj}
    res['_models']['assets'] = {
            'sprites': obj.asset_sprites.order_by('order'),
            'objects': obj.asset_objects.order_by('order'),
            'maps': obj.asset_maps.order_by('order')
        }
    res['_models'] = [obj] + list(obj.asset_sprites.order_by('order')) + \
            list(obj.asset_objects.order_by('order')) + \
            list(obj.asset_maps.order_by('order'))
    return res

urlpatterns = service.urls()

# vim: et sw=4 sts=4
