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

def unique_name(type, name):
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    if name in names:
        i = 1
        while name + '_' + str(i) in names:
            i += 1
        name += '_' + str(i)
    return name

def new(type,defaults):
    name = type.title().rstrip('s')
    name = unique_name(type, name)

    values = {'pid':drupal.pid,'name':name}
    values.update(defaults)
    drupal.db.insert_dict(type, values)
    id = drupal.db.execute('select LAST_INSERT_ID()')[0][0]
    load(type, id)

def clone(type, id):
    id = int(id)
    # for now limit to assets in this project
    res = drupal.db.find_dict(type, {'id':id,'pid':drupal.pid})
    if not res:die('Invalid source asset')
    object = res[0]
    name = object['name'] + '_Copy'
    name = unique_name(type, name)
    del object['id']
    object['name'] = name
    drupal.db.insert_dict(type, object)
    id = drupal.db.execute('select LAST_INSERT_ID()')[0][0]
    load(type, id)

def load(type, id):
    id = int(id)
    result = drupal.db.find_dict(type, {'pid':drupal.pid, 'id':id})
    if not result:return die('Asset not found: %s'%id)
    print 'Content-type:text/plain\n'
    print result[0]

def rename(type, id, new):
    id = int(id)
    names = list(x[0] for x in drupal.db.find(type, {'pid':drupal.pid}, ['name']))
    if new in names:
        return die('Duplicate name')
    if not isvalidname(new):
        return die('Invalid name')
    print 'updating... %s %s to %s'%(type,id,new)
    drupal.db.update(type, {'name':new}, {'id':id, 'pid':drupal.pid})
    exit()

def delete(type, id):
    id = int(id)
    drupal.db.delete(type, {'id':id, 'pid':drupal.pid})
    exit()

def save_order(type, order):
    '''structure looks like:
        [id1,id2,['folder',id3,id4],id5,['empty_folder']]'''
    drupal.db.update('projects', {type+'_order':order}, {'pid':drupal.pid})
    exit()

def set_attr(type, id, attr, value):
    id = int(id)
    drupal.db.update(type, {attr:json.loads(value)}, {'id':id,'pid':drupal.pid})
    exit()

def import_asset(type, id, pid):
    id = int(id)
    object = drupal.db.find_dict(type, {'id':id,'pid':drupal.pid})[0]
    object['pid'] = pid
#    del object['id']
    return die('Not implemented')
    drupal.db.insert_dict(type, object)

def _set_attr(type, id, attr, value):
    id = int(id)
    drupal.db.update(type, {attr:value}, {'id':id,'pid':drupal.pid})
    exit()

def _get_attr(type, id, attr):
    id = int(id)
    return drupal.db.find(type, {'id':id,'pid':drupal.pid}, [attr])[0][0]
