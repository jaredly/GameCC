#!/usr/bin/env python

from gcc_projects.models import Project

def new(request, pid, name, ModelClass, **defaults):
    proj = Project.objects.get(pk=pid)
    i = 1
    while 1:
        try:ModelClass.objects.get(project=proj, title="%s %d" % (name, i))
        except ModelClass.DoesNotExist:break
        i += 1
    folder = proj.load_folder(name.lower())
    asset = ModelClass(title="%s %d" % (name, i), **defaults)
    asset.project = proj
    asset.save()
    folder.append(asset.pk)
    proj.save_folder(name.lower(), folder)
    return {'_models':[asset]}

# vim: et sw=4 sts=4
