import os
import string
import json

from cgitools import exit,die
import drupal
# good: Jan 4
def isvalidname(x):
    for c in x:
        if c not in string.ascii_letters+string.digits+'_':
            return False
    return True

def last_order(type):
    lasset = drupal.db.find(type, {'pid':drupal.pid,'folder':''}, ['_index'], order='_index')
    if not lasset:lasset = 0
    else:lasset = lasset[-1][0]
    lfolder = drupal.db.find('folders', {'pid':drupal.pid,'folder':'','type':type}, ['_index'], order='_index')
    if not lfolder:lfolder = 0
    else:lfolder = lfolder[-1][0]
    return max(lasset,lfolder)

def new(type,defaults):
    name = type.title().rstrip('s')
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    i = 1
    while name + '_' + str(i) in names:
        i += 1
    name += '_' + str(i)

    values = {'pid':drupal.pid,'name':name,'_index':last_order(type),'folder':''}
    values.update(defaults)
    drupal.db.insert_dict(type, values)
    load(type, name)

def clone(type, name):
    oname = name
    name = name + '_Copy'
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    if oname not in names:
        return die('Invalid source asset: %s'%oname)
    if name in names:
        i = 1
        while name + '_' + str(i) in names:
            i += 1
        name += '_' + str(i)
    object = drupal.db.find_dict(type, {'name':oname,'pid':drupal.pid})[0]
    object['name'] = name
    drupal.db.insert_dict(type, object)
    load(type, name)

def load(type, name):
    result = drupal.db.find_dict(type, {'pid':drupal.pid, 'name':name})
    if not result:die('Asset not found: %s'%name)
    print 'Content-type:text/plain\n'
    print result[0]

def rename(type, name, new):
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    if new in names or name == new:
        return die('Duplicate name')
    if not isvalidname(new):
        return die('Invalid name')
    drupal.db.update(type, {'name':new}, {'name':name, 'pid':drupal.pid})
    exit()

def delete(type, name):
    drupal.db.delete(type, {'name':name, 'pid':drupal.pid})
    exit()

def save_order(type, names, folder):
    '''structure looks like:
        ['asset1','asset2','folder/','asset3']'''
    for i,name in enumerate(json.loads(names)):
        if name.endswith('/'):
            drupal.db.update('folders', {'_index':i, 'folder':folder}, {'name':name[:-1], 'pid':drupal.pid, 'type':type})
        else:
            drupal.db.update(type, {'_index':i,'folder':folder}, {'name':name, 'pid':drupal.pid})
    exit()

remove = delete

def set_attr(type, name, attr, value):
    drupal.db.update(type, {attr:json.loads(value)}, {'name':name})
    exit()

def import_asset(type, name, pid):
    object = drupal.db.find_dict(type, {'name':name,'pid':drupal.pid})[0]
    object['pid'] = pid
    return die('Not implemented')
    drupal.db.insert_dict(type, object)

def _set_attr(type, name, attr, value):
    drupal.db.update(type, {attr:value}, {'name':name})
    exit()

def _get_attr(type, name, attr):
    return drupal.db.find(type, {'name':name,'pid':drupal.pid}, [attr])[0][0]
