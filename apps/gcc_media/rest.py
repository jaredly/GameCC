#!/usr/bin/env python
from django.conf.urls.defaults import *
from django.conf import settings

from models import Image, Font, Sound
from restive import Service

service = Service()

@service.add(name='list')
def list_all(request):
    return {'_models': list(request.user.gcc_images.all().order_by('pk')) +
            list(request.user.gcc_fonts.all().order_by('pk')) +
            list(request.user.gcc_sounds.all()),
            'media_url':settings.MEDIA_URL}

@service.add(name='remove')
def remove_(request, type, pk):
    if type == 'image':
        Image.objects.get(pk=pk).delete()
        return {}
    else:
        raise Exception('Unsupported type')

urlpatterns = service.urls()

# vim: et sw=4 sts=4
