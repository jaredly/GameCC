import asset

import os,glob
from urllib import urlopen as upen
import json

from cgitools import exit,die
import drupal

#good: Jan 4

type = 'images'
def new():
    return asset.new(type,{'speed':1,'subimages':[]})

def clone(id):
    return asset.clone(type,id)

def load(id):
    return asset.load(type,id)

def rename(id,new):
    return asset.rename(type,id,new)

def delete(id):
    return asset.delete(type,id)

def save_order(order):
    return asset.save_items(type,order)

def set_attr(id, attr, value):
    return asset.set_attr(type, id, attr, value)

'''
def fromurl(project,url):
  id = url.split('/')[-1]
  saveraw(project, id, upen(url).read())
  exit({'id':id})

def saveraw(project,id,data):
  if os.path.isfile(os.path.join('../projects',project,'images',id)):
    parts = id.split('.')
    id = '.'.join(parts[:-1])
    ext = parts[-1]
    i=1
    while os.path.isfile(os.path.join('../projects',project,'images',id+'-'+str(i)+'.'+ext)):
      i+=1
    id += '-'+str(i)+'.'+ext
  open(os.path.join('../projects',project,'images',id),'w').write(data)

def importimages(project,urls):
  urls = json.loads(urls)
  for src in urls:
    src = os.path.join('..',src)
    saveraw(project, src.split('/')[-1], open(src).read())
  exit()

def loadraw(project):
  exit({'images':list(x.split('/')[-1] for x in glob.glob('../projects/'+project+'/images/*.*') if x.split('.')[-1] in ('png','gif','jpg'))})
'''
