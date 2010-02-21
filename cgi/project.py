import os
import sys
import string
import compile
import random
import subprocess
import myjson as json

from cgitools import exit,die
import drupal

#todo: Jan 4

def execute(cmd):
    p = subprocess.Popen(cmd, shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, close_fds=True)
    stdout, stderr = (p.stdout.read(), p.stderr.read())
    if stderr or stdout:
        die(stdout + stderr)

def list_projects():
    projects = [x[0] for x in drupal.db.find('projects',{'uid':drupal.uid},['name'])]
    exit({'projects':projects});

import glob

def list_images():
    images = drupal.db.find_dict('projects', {'pid':drupal.pid})[0]['images']
    exit({'images':images})

def add_images(images):
    oldimages = drupal.db.find_dict('projects', {'pid':drupal.pid})[0]['images']
    oldimages += json.loads(images)
    drupal.db.update('projects',{'images':oldimages},{'pid':drupal.pid})
    exit()

def list_all_images():
    exit({'images':os.listdir('../raw_images')})

noproject = ['project/new','project/list_projects','project/load_plugins']

def new(name):
    if name in [x[0] for x in drupal.db.find('projects',{'uid':drupal.uid},['name'])]:
        return die('duplicate name')
    object = {'uid':drupal.uid,
        'name':name,
        'images':[],
        'config':'',
        'images_order':[],
        'objects_order':[],
        'maps_order':[]}
    drupal.db.insert_dict('projects',object)
    drupal.pid = drupal.db.execute('select LAST_INSERT_ID()')[0][0]
    load(name)

def remove(project):
    dct = _load()
    ## move to trash?
    drupal.db.execute('delete from projects where pid=%d'%drupal.pid)
    drupal.db.execute('delete from images where pid=%d'%drupal.pid)
    drupal.db.execute('delete from objects where pid=%d'%drupal.pid)
    drupal.db.execute('delete from maps where pid=%d'%drupal.pid)
    exit()

def _load():
    result = drupal.db.execute_dict('select * from projects where pid=%d'%drupal.pid)[0]
    images = drupal.db.execute_dict('select * from images where pid=%d order by _index'%drupal.pid)
    objects = drupal.db.execute_dict('select * from objects where pid=%d order by _index'%drupal.pid)
    maps = drupal.db.execute_dict('select * from maps where pid=%d order by _index'%drupal.pid)
    return {'images':images,'objects':objects,'maps':maps,'project':result}

def load(name):
    drupal.pid = drupal.db.find('projects',{'name':name,'uid':drupal.uid},['pid'])[0][0]
    exit(_load())

def uploadimage(project,file):
    die('not implemented')
    path = os.path.join('../raw_images',file.filename)
    if os.path.exists(path):
        i = 1
        while os.path.exists('.'.join(path.split('.')[:-1]) + '_%d.%s'%(i,path.split('.')[-1])):
            i += 1
        path = '.'.join(path.split('.')[:-1]) + '_%d.%s'%(i,path.split('.')[-1])
    open(path, 'w').write(file.value)
    filename = path.split('/')[-1]
    raws = drupal.db.find('projects',{'pid':drupal.pid},['images'])[0][0]
    if not raws:raws = []
    raws.append(filename)
    drupal.db.update('projects',{'images':raws},{'pid':drupal.pid})
    raws = drupal.db.find('projects',{'pid':drupal.pid},['images'])[0][0]
    sys.stdout.write(filename)

def preview(pid):
    die('notimplemented')
    compiler = compile.Compiler(pid)
    name = compiler.compile('haxe')
    data = {'name':name,'width':compiler.width,'height':compiler.height,'fps':40,'color':'ffffff'}
    cmd = '~/haxe -swf ../preview/%(name)s.swf -main %(name)s -swf-version 9 -swf-header %(width)s:%(height)s:%(fps)s:%(color)s'%data
    execute(cmd)
    execute('cat ../data/default.html | sed -e "s/<<NAME>>/%(name)s/g" -e "s/<<TITLE>>/%(name)s/g" -e "s/<<WIDTH>>/%(width)s/g" -e "s/<<HEIGHT>>/%(height)s/g" -e "s/<<COLOR>>/%(color)s/g" > ../preview/%(name)s.html'%data)
    exit({'name':name,'width':compiler.width,'height':compiler.height})
