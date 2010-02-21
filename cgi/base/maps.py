import asset

from cgitools import exit,die
import drupal

import json

#good: Jan 4

type = 'maps'
def new():
    return asset.new(type,{'objects':[],'width':500,'height':500,'events':{},'tiles':[],'views':[],'background':None})

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

#check

def _new_item(id,object,x,y):
  objects = asset._get_attr('maps',id,'objects')
  objects.append({'id':object,'x':int(float(x)),'y':int(float(y))})
  asset._set_attr('maps', id, 'objects', objects)
  exit()

def add_item(id, item):
  item = json.loads(item)
  objects = asset._get_attr('maps',id,'objects')
  objects.append(item)
  asset._set_attr('maps', id, 'objects', objects)

def remove_item(id, item):
  item = json.loads(item)
  objects = asset._get_attr('maps',id,'objects')
  objects.remove(item)
  asset._set_attr('maps', id, 'objects', objects)

'''def _remove_item(id,object,x,y):
  objects = asset._get_attr('maps',id,'objects')
  for i in range(len(objects)):
    if objects[i]['id']==object and items[i]['x']==int(float(x)) and items[i]['y']==int(float(y)):
      objects.pop(i)
      break
  asset._set_attr('maps', id, 'objects', objects)
  exit()'''

def save_items(id,items):
  objects = json.loads(items)
  asset._set_attr('maps', id, 'objects', objects)
