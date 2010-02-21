import asset

from cgitools import exit,die
import drupal

import myjson as json

#good: Jan 4

type = 'objects'
def new():
    return asset.new(type,{'visible':False,
        'image':None,'events':{},
        'attributes':{},'parent':'BaseObject'})

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

#tocheck

def save_actions(id,event,actions):
  events = asset._get_attr('objects',id,'events')
  events[event] = json.loads(actions)
  asset._set_attr('objects',id,'events', events)

## try return the actions list via json??

def add_event(id,event):
  events = asset._get_attr('objects',id,'events')
  events[event] = []
  asset._set_attr('objects',id,'events', events)

def remove_event(id,event):
  events = asset._get_attr('objects',id,'events')
  del events[event]
  asset._set_attr('objects',id,'events', events)

def duplicate_event(id,event,nevent):
  events = asset._get_attr('objects',id,'events')
  events[nevent] = events[event]
  asset._set_attr('objects', id, 'events', events)
  return events[nevent]

def change_event(id,event,nevent):
  events = asset._get_attr('objects',id,'events')
  events[nevent] = events[event]
  del events[event]
  asset._set_attr('objects', id, 'events', events)
  return events[nevent]

