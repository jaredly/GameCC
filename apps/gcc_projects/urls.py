#!/usr/bin/env python
from django.conf.urls.defaults import *

import inspect

from django.utils import simplejson as json

from models import Project

from django.core import serializers
from django.http import HttpResponse

class Rest:
    def __init__(self):
        self.url_list = []

    def add(self, function):
        def meta(request):
            try:
                data = json.loads(request.POST['data'])
            except:
                res = {'error': 'invalid arguments'}
            try:
                res = function(request, **data)
            except TypeError:
                res = {'error':'invalid arguments'}
            except Exception,e:
                res = {'error':str(e)}
            else:
                if not res.has_key('error'):
                    res['error'] = None
            if res.has_key('_models'):
                res['_models'] = serializers.serialize('json', res['_models'], use_natural_keys=True)
            return HttpResponse(json.dumps(res))
        self.url_list.append(['^' + function.__name__ + '/$', meta])

    def urls(self):
        return patterns('', *self.url_list)

service = Rest()

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
