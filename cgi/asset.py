import os
import string
import myjson as json

from cgitools import exit,die
import drupal

def isvalidname(x):
    for c in x:
        if c not in string.ascii_letters+string.digits+'_':
            return False
    return True

def new(type, project):
    name = type.title().rstrip('s')
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    i = 1
    while name + '_' + str(i) in names:
        i += 1
    name += '_' + str(i)
    values = {'uid':drupal.uid,'name':name,'pid':drupal.pid,'tags':'','aorder':len(names),'folder':''}
    values.update(defaults[type])
    drupal.db.insert_dict(type, values)
    load(type, project, name)

def clone(type, project, name):
    oname = name
    name = name + '_Copy'
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    if oname not in names:
        return die('Invalid source asset')
    if name in names:
        i = 1
        while name + '_' + str(i) in names:
            i += 1
        name += '_' + str(i)
    values = {'uid':drupal.uid, 'name':name, 'pid':drupal.pid, 'tags':'','aorder':len(names),'folder':''}
    values.update(drupal.db.find_dict(type, {'name':oname,'pid':drupal.pid})[0])
    drupal.db.insert_dict(type, values)
    load(type, project, name)

def load(type, project, name):
    result = drupal.db.find_dict(type, {'pid':drupal.pid, 'name':name})
    if not result:die('asset not found')
    print result[0]

def rename(type, project, name, new):
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    if new in names or name == new:
        return die('Duplicate name')
    if not isvalidname(new):
        return die('Invalid name')
    drupal.db.update(type, {'name':new}, {'name':name, 'pid':drupal.pid})
    exit()

def delete(type, project, name):
    drupal.db.delete(type, {'name':name, 'pid':drupal.pid})
    exit()

def save_order(type, project, names):
    for i,name in enumerate(json.loads(names)):
        #print names,i,name
        drupal.db.update(type, {'aorder':i}, {'name':name, 'pid':drupal.pid})
    exit()

remove = delete

def set_attr(type, project, name, attr, value):
    drupal.db.update(type, {attr:json.loads(value)}, {'name':name})
    exit()

def _set_attr(type, project, name, attr, value):
    drupal.db.update(type, {attr:value}, {'name':name})
    exit()

def _get_attr(type, project, name, attr):
    return drupal.db.find(type, {'name':name}, [attr])[0][0]

defaults = {
    'images':{'subimages':[],'speed':1.0},
    'objects':{'image':None,'visible':True,'events':{},'attributes':[],'parent':'BaseObject'},
    'maps':{'width':500,'height':500,'objects':[],'tiles':[],'events':{}}
    # add persistant
}

defaults = {
    'images':{'subimages':[],'speed':1.0},
    'maps':{'width':500, 'height':500, 'persistant': False, 'items':[]},
    'objects':{'visible':True, 'solid':False, 'image':'', 'events':{}, 'parent':'BaseObject'},
}
