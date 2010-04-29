'''maps.py handles the Map type asset

>>> map = new()
>>> map['id']
1
>>> id = map['id']
>>> map['name']
u'Map'
>>> add_item(id, {'id':1, 'x':0, 'y':0})
>>> load(id)['objects']
[{u'y': 0, u'x': 0, u'id': 1}]
>>> remove_item(id, {'id':1, 'x':0, 'y':0})
>>> load(id)['objects']
[]
>>> add_item(id, {'id':2, 'x':10, 'y':30})

'''

import asset
import drupal

class ItemError(Exception):pass

class MapManager(asset.AssetManager):
    atype = 'maps'
    defaults = {'objects':[],'width':500,'height':500,'events':{},'tiles':[],'views':[],'background':None}

    @classmethod
    def add_item(cls, id, item):
        objects = cls._get_attr(id, 'objects')
        objects.append(item)
        cls._set_attr(id, 'objects', objects)

    @classmethod
    def remove_item(cls, id, item):
        objects = cls._get_attr(id, 'objects')
        if item in objects:
            objects.remove(item)
        else:
            raise ItemError("Item not found in map #%d; %s"%(id, item))
        cls._set_attr(id, 'objects', objects)

    @classmethod
    def save_items(cls, id, items):
        cls._set_attr(id, 'objects', items)

'''def _remove_item(id,object,x,y):
  objects = asset._get_attr('maps',id,'objects')
  for i in range(len(objects)):
    if objects[i]['id']==object and items[i]['x']==int(float(x)) and items[i]['y']==int(float(y)):
      objects.pop(i)
      break
  asset._set_attr('maps', id, 'objects', objects)
  exit()'''
