#!/usr/bin/env python

import magic
from ..base import drupal
from ..base import maps

class Test(magic.MagicTest):

    def newMap(self):
        self.assertEquals(maps.list(), [])
        map = maps.new()
        self.assertEquals(map['name'], 'Map')
        self.mid = map['id']

    def addItem(self):
        self.assertEquals(maps.load(self.mid)['objects'], [])
        obj = {'id':2, 'x':23, 'y':12}
        maps.add_item(self.mid, obj)
        self.assertEquals(maps.load(self.mid)['objects'], [obj])
        self.assertThrows(maps.ItemError, maps.remove_item, self.mid, {'mod':2})
        maps.remove_item(self.mid, obj)
        self.assertEquals(maps.load(self.mid)['objects'], [])

    def saveItems(self):
        self.assertEquals(maps.load(self.mid)['objects'], [])
        objs = [{'id':2,'x':10,'y':2},
                {'id':3,'x':14,'y':17}]
        maps.save_items(self.mid, objs)
        self.assertEquals(maps.load(self.mid)['objects'], objs)


# vim: et sw=4 sts=4
