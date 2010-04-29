'''handles all projects
'''
import os
import sys
import imghdr
import string
import random
import subprocess

import drupal

RAW_IMG_DIR = os.path.join(os.path.dirname(__file__),'../../raw_images')

class ImageError(Exception):pass

def list_projects():
    projects = [x[0] for x in drupal.db.find('projects',{'uid':drupal.uid},['name'])]
    return projects

def list_images():
    images = drupal.db.find_dict('projects', {'pid':drupal.pid})[0]['images']
    return images

def add_images(images):
    allimgs = list_all_images()
    for img in images:
        if not img in allimgs:
            raise ImageError('image not found')
    oldimages = drupal.db.find_dict('projects', {'pid':drupal.pid})[0]['images']
    oldimages += images
    drupal.db.update('projects',{'images':oldimages},{'pid':drupal.pid})

def list_all_images():
    return os.listdir(RAW_IMG_DIR)

def new(name):
    if name in [x[0] for x in drupal.db.find('projects',{'uid':drupal.uid},['name'])]:
        return False
    object = {'uid':drupal.uid,
        'name':name,
        'images':[],
        'config':'',
        'images_order':[],
        'objects_order':[],
        'maps_order':[]}
    drupal.db.insert_dict('projects',object)
    drupal.pid = drupal.db.execute('select LAST_INSERT_ID()')[0][0]
    return load()

def remove():
    dct = load()
    ## move to trash?
    drupal.db.execute(
            'delete from projects where pid=%d'%drupal.pid)
    drupal.db.execute(
            'delete from images where pid=%d'%drupal.pid)
    drupal.db.execute(
            'delete from objects where pid=%d'%drupal.pid)
    drupal.db.execute(
            'delete from maps where pid=%d'%drupal.pid)

def load():
    result = drupal.db.execute_dict('select * from projects where pid=%d'%drupal.pid)[0]
    images = drupal.db.execute_dict('select * from images where pid=%d order by _index'%drupal.pid)
    objects = drupal.db.execute_dict('select * from objects where pid=%d order by _index'%drupal.pid)
    maps = drupal.db.execute_dict('select * from maps where pid=%d order by _index'%drupal.pid)
    return {'images':images,'objects':objects,'maps':maps,'project':result}

def uploadimage(filename, value):
    path = os.path.join(RAW_IMG_DIR, filename)
    itype = imghdr.what(filename, value) 
    if not itype or itype not in ('jpeg','gif','png'):
        return None
    if itype == 'jpeg':
        itype = 'jpg'
    basename = '.'.join(filename.split('.')[:-1])
    if not basename:
        return None
    filename = '%s.%s'%(basename, itype)
    path = os.path.join(RAW_IMG_DIR,
            filename)
    
    if os.path.exists(path):
        i = 1
        while os.path.exists(os.path.join(RAW_IMG_DIR,
            basename + '_%d.%s'%(i,itype))):
            i += 1
        path = os.path.join(RAW_IMG_DIR,
            basename + '_%d.%s'%(i,itype))
        filename = '%s_%d.%s'%(basename, i, itype)

    open(path, 'w').write(value)
    raws = drupal.db.find('projects',
            {'pid':drupal.pid},['images'])[0][0]
    if not raws:raws = []
    raws.append(filename)
    drupal.db.update('projects',
            {'images':raws},{'pid':drupal.pid})
    return filename


