'''objects.py -- does most of the heavly lifting
here, handles the 'object' asset type

>>> id = new()['id']
>>> id
1
>>> id = clone(id)['id']
>>> id
2
>>> add_event(id, 'keydown')
>>> remove_event(id, 'mouseup')
Traceback (most recent call last):
...
KeyError: 'mouseup'
>>> load(id)['events']
{u'keydown': []}
>>> remove_event(id, 'keydown')
>>> add_event(id, 'keydown')
>>> save_actions(id, 'keydown', ['something'])
>>> duplicate_event(id, 'keydown', 'mouseup')
[u'something']
>>> events = load(id)['events']
>>> events['keydown'] == events['mouseup']
True

'''
import asset

from cgitools import exit,die
import drupal

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

def save_actions(id,event,actions):
  events = asset._get_attr('objects',id,'events')
  events[event] = actions
  asset._set_attr('objects',id,'events', events)

