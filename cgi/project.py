

## project.py

import os
import sys
import string
import compile
import random
import subprocess
import myjson as json

from utils import exit,die,drupal

def execute(cmd):
  p = subprocess.Popen(cmd, shell=True,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
  (child_stdout,
   child_stderr) = (p.stdout.read(), p.stderr.read())
  if child_stderr or child_stdout:
    die(child_stdout+child_stderr)

def list_projects():
  projects = [x[0] for x in drupal.db.execute('select name from projects where uid=%d'%drupal.uid)]
  exit({'projects':projects});
  
import glob

def load_plugins():
  plugins = glob.glob('../plugins/*/*.info')
  exit({'plugins':list(x.split('/')[-1][:-len('.info')] for x in plugins if x.split('/')[-1][:-len('.info')]!='example')});

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

def new(project):
  if drupal.pid:
    die('duplicate name')
  else:
    drupal.db.insert('projects',(None, drupal.uid, project, '', 0, '', []))
    #drupal.db.execute("insert into projects values (NULL, %d, '%s', '', 0, '', '')" % (drupal.uid, project))
    #drupal.db.commit()
  drupal.getpid(project)
  load(project)

def remove(project):
  dct = _load()
  drupal.db.execute('delete from projects where pid=%d'%drupal.pid)
  drupal.db.execute('delete from images where pid=%d'%drupal.pid)
  drupal.db.execute('delete from objects where pid=%d'%drupal.pid)
  drupal.db.execute('delete from maps where pid=%d'%drupal.pid)
  exit()


def _load():
  result  = drupal.db.execute_dict('select * from projects where pid=%d'%drupal.pid)[0]
  images  = drupal.db.execute_dict('select * from images  where pid=%d order by aorder'%drupal.pid)
  objects = drupal.db.execute_dict('select * from objects where pid=%d order by aorder'%drupal.pid)
  maps    = drupal.db.execute_dict('select * from maps    where pid=%d order by aorder'%drupal.pid)
  return {'images':images,'objects':objects,'maps':maps,'project':result}

def load(*a):
  exit(_load())

def uploadimage(project,file):
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

def preview(project):
  compiler = compile.Compiler(project)
  name = compiler.compile('haxe')
  data = {'name':name,'width':compiler.width,'height':compiler.height,'fps':40,'color':'ffffff'}
  cmd = '~/haxe -swf ../preview/%(name)s.swf -main %(name)s -swf-version 9 -swf-header %(width)s:%(height)s:%(fps)s:%(color)s'%data
  execute(cmd)
  execute('cat ../data/default.html | sed -e "s/<<NAME>>/%(name)s/g" -e "s/<<TITLE>>/%(name)s/g" -e "s/<<WIDTH>>/%(width)s/g" -e "s/<<HEIGHT>>/%(height)s/g" -e "s/<<COLOR>>/%(color)s/g" > ../preview/%(name)s.html'%data)
  
  exit({'name':name,'width':compiler.width,'height':compiler.height})

'''
projbase = '../projects/'

def randname():
  ret = ''
  for i in range(10):
    ret += random.choice(string.ascii_lowercase)
  return ret.title()

def execute(x):
  p = subprocess.Popen(x, shell=True,
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
  return p.stdout.read()+p.stderr.read()

def list_images(project):
  exit({'images':sorted(list(x for x in os.listdir(os.path.join(projbase, project, 'images')) if x.split('.')[-1].lower() in ('png','gif','jpg')))})

## callbacks

def uploadimage(project,file):
  open(os.path.join(projbase,project,'images',file.filename),'w').write(file.value)
  sys.stdout.write(file.filename)

def addsvg(project,data,bbox=None):
  i = 1
  while os.path.exists(os.path.join(projbase,project,'images','custom%d.svg'%i)):
    i+=1
  name = os.path.join(projbase,project,'images','custom%d.svg'%i)
  open(name, 'w').write(data)
  exit({})
  

def load(project):
  objects = sorted(list(x for x in os.listdir(os.path.join(projbase, project, 'objects')) if x.split('.')[-1]=='info'))
  maps = sorted(list(x for x in os.listdir(os.path.join(projbase, project, 'maps')) if x.split('.')[-1]=='info'))
  images = sorted(list(x for x in os.listdir(os.path.join(projbase, project, 'images')) if x.split('.')[-1]=='info'))
  rimages = sorted(list(x for x in os.listdir(os.path.join(projbase, project, 'images')) if x.split('.')[-1].lower() in ('png','gif','jpg')))
  exit({'objects':objects,'maps':maps,'images':images,'raw_images':rimages,'info':{'name':project}});

def preview(project):
  name = compile.Compiler(project).compile('haxe')
  res = execute('./compile.sh "%s.hx" "%s"'%(name,name))#.read()
  if res:
    die(res)
  res = execute('mv "%s.hx" "%s.hx.swf" "%s.hx.html" "../projects/%s/preview/"'%(name,name,name,project))
  if res:
    die(res)
  exit({'url':'projects/'+project+'/preview/'+name+'.hx.html','name':name})

def killpreview(project, name):
  res = execute('rm ../projects/%s/preview/%s*'%(project.replace(' ','\\ '),name))
  if res:die(res)
  exit()

def rename(project, to):
  if not os.path.exists('../projects/'+to):
    os.rename('../projects/'+project,'../projects/'+to)
    exit({'nname':to})
  else:
    exit({'nname':project})

def delete(project):
  res = execute('rm -r ../projects/%s'%project)
  if res:
    die(res)
  else:
    exit({})

remove = delete

import glob

def load_plugins():
  plugins = glob.glob('../plugins/*/*.info')
  exit({'plugins':list(x.split('/')[-1][:-len('.info')] for x in plugins if x.split('/')[-1][:-len('.info')]!='example')});

def new():
  base = projbase + 'Project%d'
  i=1
  while os.path.isdir(base%i):
    i+=1
  name = base%i
  os.mkdir(name)
  for fold in ['images','objects','maps','preview']:
    os.mkdir(os.path.join(name,fold))
  load('Project%d'%i)

def clone(project):
  nname = project + '_Clone'
  if os.path.exists(projbase + project):
    i=2
    while os.path.isdir(projbase+nname+str(i)):
      i+=1
    nname = nname+str(i)
  os.system('cp -r "%s" "%s"'%(projbase+project,projbase+nname))
  exit({'name':nname})


def list_projects():
  exit({'projects':sorted(x for x in os.listdir('../projects/') if not x[0]=='.')});
'''

