#!/usr/bin/env python
from django.conf.urls.defaults import *
from django.conf import settings

# from models import Image, Font, sound
from gameccorg.rest import Rest

service = Rest()

@service.add(name='list')
def list_all(request):
    return {'_models': list(request.user.gcc_images.all()) +
            list(request.user.gcc_fonts.all()) +
            list(request.user.gcc_sounds.all()),
            'media_url':settings.MEDIA_URL}

urlpatterns = service.urls()

# vim: et sw=4 sts=4
