import asset

from cgitools import exit,die
import drupal

import myjson as json

type = 'objects'
def new():
    return asset.new(type,{'visible':False,'image':None,'events':{},'attributes':{},'parent':'BaseObject'})

def clone(name):
    return asset.clone(type,name)

def load(name):
    return asset.clone(type,name)

def rename(name,new):
    return asset.clone(type,name)

def delete(name):
    return asset.delete(type,name)

def save_order(names,folder):
    return asset.save_items(type,names,folder)


def save_actions(project,name,event,actions):
  events = asset._get_attr('objects',project,name,'events')
  events[event] = json.loads(actions)
  asset._set_attr('objects',project,name,'events', events)
  exit()

def add_event(project,name,event):
  events = asset._get_attr('objects',project,name,'events')
  events[event] = []
  asset._set_attr('objects',project,name,'events', events)
  exit()

def remove_event(project,name,event):
  events = asset._get_attr('objects',project,name,'events')
  del events[event]
  asset._set_attr('objects',project,name,'events', events)
  exit()

def duplicate_event(project,name,event,nevent):
  events = asset._get_attr('objects',project,name,'events')
  events[nevent] = events[event]
  asset._set_attr('objects', project, name, 'events', events)
  exit({'actions':events[nevent]})

def change_event(project,name,event,nevent):
  events = asset._get_attr('objects',project,name,'events')
  events[nevent] = events[event]
  del events[event]
  asset._set_attr('objects', project, name, 'events', events)
  exit({'actions':events[nevent]})

