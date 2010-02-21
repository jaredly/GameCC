import os
import sys
import string
import compile
import random
import subprocess
import myjson as json

from cgitools import exit,die
import drupal

RAW_IMG_DIR = os.path.join(os.dirname(__file__),'../../rawimages')

def list_projects():
    projects = [x[0] for x in drupal.db.find('projects',{'uid':drupal.uid},['name'])]
    return projects

def list_images():
    images = drupal.db.find_dict('projects', {'pid':drupal.pid})[0]['images']
    return images

def add_images(images):
    oldimages = drupal.db.find_dict('projects', {'pid':drupal.pid})[0]['images']
    oldimages += json.loads(images)
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
    return True

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

def check_type(file):
    image_type = 
    if not image_type

def uploadimage(file):
    path = os.path.join(RAW_IMG_DIR,file.filename)
    itype = imghdr.what(file.filename, file.value) 
    if not itype or itype not in ('jpeg','gif','png'):
        return None
    if itype == 'jpeg':
        itype = 'jpg'
    basename = '.'.join(file.filename.split('.')[:-1])
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
        path = os.path.join(path,
            basename + '_%d.%s'%(i,itype))
        filename = '%s_%d.%s'%(basename, i, itype)

    open(path, 'w').write(file.value)
    raws = drupal.db.find('projects',
            {'pid':drupal.pid},['images'])[0][0]
    if not raws:raws = []
    raws.append(filename)
    drupal.db.update('projects',
            {'images':raws},{'pid':drupal.pid})
    return filename


