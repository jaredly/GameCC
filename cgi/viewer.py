import os
import sys
import string
import myjson as json
import tarfile
import StringIO

import compile

from cgitools import exit,die
import drupal

#good: Jan 4

from project import list_projects

def dist(project):
    comp = compile.Compiler(project)
    text, data = comp.compile('python',False)
    name = comp.genName()
    sio = StringIO.StringIO()
    tf = tarfile.open(name+'.tbz','w:bz2')
    open(name+'.py','w').write(text)
    tf.add(name+'.py')
    images = json.loads(data['images_more'])
    for i in images:
        tf.add(os.path.join('..','raw_images',i))
    tf.close()
    sys.stdout.write(open(name+'.tbz').read())
    os.remove(name+'.py')
    os.remove(name+'.tbz')

#def addfake(tf,name,txt):
#    fl = StringIO.StringIO(txt)
#    info = tarfile.TarInfo.frombuf(txt)
#    tf.addfile(info,fl)

