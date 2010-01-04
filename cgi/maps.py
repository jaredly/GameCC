import asset

from cgitools import exit,die
import drupal

import myjson as json

def _new_item(project,name,object,x,y):
  items = asset._get_attr('maps',project,name,'items')
  items.append({'name':object,'x':int(float(x)),'y':int(float(y))})
  asset._set_attr('maps', project, name, 'items', items)
  exit()

def add_item(project, name, item):
  item = json.loads(item)
  items = asset._get_attr('maps',project,name,'items')
  items.append(item)
  asset._set_attr('maps', project, name, 'items', items)
  exit()

def remove_item(project, name, item):
  item = json.loads(item)
  items = asset._get_attr('maps',project,name,'items')
  items.remove(item)
  asset._set_attr('maps', project, name, 'items', items)
  exit()

def _remove_item(project,name,object,x,y):
  items = asset._get_attr('maps',project,name,'items')
  for i in range(len(items)):
    if items[i]['name']==object and items[i]['x']==int(float(x)) and items[i]['y']==int(float(y)):
      items.pop(i)
      break
  asset._set_attr('maps', project, name, 'items', items)
  exit()

def save_items(project,name,items):
  items = json.loads(items)
  asset._set_attr('maps', project, name, 'items', items)
  exit()
