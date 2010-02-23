import os
import string

import drupal

class AssetException(Exception):pass
class AssetNameException(Exception):pass

# good: Jan 4
def isvalidname(x):
    for c in x:
        if c not in string.ascii_letters+string.digits+'_':
            return False
    return True

class AssetManager:
    defaults = {}
    atype = ''

    @classmethod
    def list(cls):
        return drupal.db.find(cls.atype, {'pid':drupal.pid}, ['name'])

    @classmethod
    def new(cls):
        name = cls.atype.title().rstrip('s')
        name = cls.unique_name(name)

        values = {'pid':drupal.pid,'name':name}
        values.update(cls.defaults)
        drupal.db.insert_dict(cls.atype, values)
        id = drupal.db.execute(
                'select LAST_INSERT_ID()')[0][0]
        return cls.load(id)

    @classmethod
    def clone(cls, id):
        id = int(id)
        # for now limit to assets in this project
        res = drupal.db.find_dict(cls.atype, 
                {'id':id,'pid':drupal.pid})
        if not res:die('Invalid source asset')
        object = res[0]
        name = object['name'] + '_Copy'
        name = cls.unique_name(name)
        del object['id']
        object['name'] = name
        drupal.db.insert_dict(cls.atype, object)
        id = drupal.db.execute(
                'select LAST_INSERT_ID()')[0][0]
        return cls.load(id)

    @classmethod
    def load(cls, id):
        id = int(id)
        result = drupal.db.find_dict(cls.atype, 
                {'pid':drupal.pid, 'id':id})
        if not result:
            raise AssetException(
                    'Asset %d of type "%s" not found' %
                    (id,cls.atype))
        return result[0]

    @classmethod
    def rename(cls, id, new):
        id = int(id)
        names = cls.list()
        if new in names:
            raise AssetNameError('Duplicate name')
        if not isvalidname(new):
            raise AssetNameError('Invalid Name')
        drupal.db.update(cls.atype, {'name':new}, 
                {'id':id, 'pid':drupal.pid})

    @classmethod
    def delete(cls, id):
        id = int(id)
        drupal.db.delete(cls.atype, 
                {'id':id, 'pid':drupal.pid})

    @classmethod
    def save_order(cls, order):
        '''structure looks like:
            [id1,id2,['folder',id3,id4],id5,['empty_folder']]'''
        drupal.db.update('projects', 
                {cls.atype+'_order':order}, 
                {'pid':drupal.pid})

    @classmethod
    def set_attr(cls, id, attr, value):
        id = int(id)
        drupal.db.update(cls.atype, 
                {attr:json.loads(value)}, 
                {'id':id,'pid':drupal.pid})

    @classmethod
    def import_asset(cls, id, pid):
        id = int(id)
        object = drupal.db.find_dict(cls.atype, 
                {'id':id,'pid':drupal.pid})[0]
        object['pid'] = pid
        return die('Not implemented')
        drupal.db.insert_dict(cls.atype, object)

    @classmethod
    def _set_attr(cls, id, attr, value):
        id = int(id)
        drupal.db.update(cls.atype, {attr:value}, 
                {'id':id,'pid':drupal.pid})

    @classmethod
    def _get_attr(cls, id, attr):
        id = int(id)
        return drupal.db.find(cls.atype, 
                {'id':id,'pid':drupal.pid}, [attr])[0][0]

    @classmethod
    def unique_name(cls, name):
        '''get a unique name'''
        names = cls.list()
        if name in names:
            i = 1
            while name + ' ' + str(i) in names:
                i += 1
            name += ' ' + str(i)
        return name

