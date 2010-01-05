import asset

from cgitools import exit,die
import drupal

import myjson as json

#good: Jan 4

type = 'objects'
def new():
    return asset.new(type,{'visible':False,'image':None,'events':{},'attributes':{},'parent':'BaseObject'})

def clone(name):
    return asset.clone(type,name)

def load(name):
    return asset.load(type,name)

def rename(name,new):
    return asset.rename(type,name,new)

def delete(name):
    return asset.delete(type,name)

def save_order(names,folder):
    return asset.save_items(type,names,folder)

def set_attr(name, attr, value):
    return asset.set_attr(type, name, attr, value)

#tocheck

def save_actions(name,event,actions):
  events = asset._get_attr('objects',name,'events')
  events[event] = json.loads(actions)
  asset._set_attr('objects',name,'events', events)
  exit()

def add_event(name,event):
  events = asset._get_attr('objects',name,'events')
  events[event] = []
  asset._set_attr('objects',name,'events', events)
  exit()

def remove_event(name,event):
  events = asset._get_attr('objects',name,'events')
  del events[event]
  asset._set_attr('objects',name,'events', events)
  exit()

def duplicate_event(name,event,nevent):
  events = asset._get_attr('objects',name,'events')
  events[nevent] = events[event]
  asset._set_attr('objects', name, 'events', events)
  exit({'actions':events[nevent]})

def change_event(name,event,nevent):
  events = asset._get_attr('objects',name,'events')
  events[nevent] = events[event]
  del events[event]
  asset._set_attr('objects', name, 'events', events)
  exit({'actions':events[nevent]})

