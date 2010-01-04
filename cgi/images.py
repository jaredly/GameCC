import asset

import os,glob
from urllib import urlopen as upen
import myjson as json

from cgitools import exit,die
import drupal

'''
def fromurl(project,url):
  name = url.split('/')[-1]
  saveraw(project, name, upen(url).read())
  exit({'name':name})

def saveraw(project,name,data):
  if os.path.isfile(os.path.join('../projects',project,'images',name)):
    parts = name.split('.')
    name = '.'.join(parts[:-1])
    ext = parts[-1]
    i=1
    while os.path.isfile(os.path.join('../projects',project,'images',name+'-'+str(i)+'.'+ext)):
      i+=1
    name += '-'+str(i)+'.'+ext
  open(os.path.join('../projects',project,'images',name),'w').write(data)

def importimages(project,urls):
  urls = json.loads(urls)
  for src in urls:
    src = os.path.join('..',src)
    saveraw(project, src.split('/')[-1], open(src).read())
  exit()

def loadraw(project):
  exit({'images':list(x.split('/')[-1] for x in glob.glob('../projects/'+project+'/images/*.*') if x.split('.')[-1] in ('png','gif','jpg'))})
'''
