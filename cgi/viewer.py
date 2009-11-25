import os
import sys
import string
import myjson as json
import tarfile
import StringIO

import compile

from utils import exit,die,drupal

def list_projects():
  projects = [x[0] for x in drupal.db.execute('select name from projects where uid=%d'%drupal.uid)]
  exit({'projects':projects});

def dist(project):
  comp = compile.Compiler(project)
  text, data = comp.compile('python',False)
  name = comp.genName()
  sio = StringIO.StringIO()
  tf = tarfile.open(name+'.tbz','w:bz2')
  
  open(name+'.py','w').write(text)
  tf.add(name+'.py')
  
  #addfake(tf,project+'.py',text)
  #os.chdir('../')
  images = json.loads(data['images_more'])
  for i in images:
    tf.add(os.path.join('..','raw_images',i))
  tf.close()
  #os.chdir('cgi')
  sys.stdout.write(open(name+'.tbz').read())
  os.remove(name+'.py')
  os.remove(name+'.tbz')
  
def addfake(tf,name,txt):
  fl = StringIO.StringIO(txt)
  info = tarfile.TarInfo.frombuf(txt)
  tf.addfile(info,fl)

