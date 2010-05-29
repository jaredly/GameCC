#!/usr/bin/env python
from django.conf.urls.defaults import *

# from models import Image, Font, sound
from gameccorg.rest import Rest

service = Rest()

@service.add(name='list')
def list_all(request):
    #u = request.user
    #i = u.gcc_images.all()
    #return {'_models': list(u.gcc_images.all()) + list(u.gcc_fonts.all()) + list(u.gcc_sounds.all())}
    return {'_models': list(request.user.gcc_images.all()) + list(request.user.gcc_fonts.all()) + list(request.user.gcc_sounds.all())}

urlpatterns = service.urls()

# vim: et sw=4 sts=4
