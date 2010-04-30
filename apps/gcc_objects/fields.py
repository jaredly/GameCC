#!/usr/bin/env python

from django.db import models
from django.core.exceptions import ValidationError

 
try:
    import cPickle as pickle
except:
    import pickle
 
import base64
 
class SerializedDataField(models.TextField):
    '''modified from David Cramer's version
    http://www.davidcramer.net/code/181/custom-fields-in-django.html
    '''
    __metaclass__ = models.SubfieldBase
 
    def to_python(self, value):
        if value is None: return
        if not isinstance(value, basestring): return value
        value = pickle.loads(base64.b64decode(value))
        return value
 
    def get_prep_save(self, value):
        if value is None: return
        return base64.b64encode(pickle.dumps(value))

    def get_prep_lookup(self, lookup_type, value):
        # No lookups supported
        raise TypeError('Lookup type %r not supported.' % lookup_type)
    
    def formfield(self, **kwargs):
        defaults = {'form_class': self.FORMFIELD}
        defaults.update(kwargs)
        return super(HandField, self).formfield(**defaults)

class BaseField(models.TextField):
    WIDGET = None

    def formfield(self, **kwargs):
        defaults = {}
        if self.WIDGET:
            defaults = {'widget': self.WIDGET}
        defaults.update(kwargs)
        return super(BaseField, self).formfield(**defaults)

    def clean(self, value, model_instance):
        try:
            type, rest = value.split(':', 1)
            if type == 'c':
                if utils.const_type(rest) != self.main_type():
                    raise ValidationError('invalid constant')
                return value
            obj = model_instance.event.object.title
            if type == 'p':
                num, var = rest.split(':')
                if utils.get_type(obj, var) != self.main_type():
                    raise ValidationError('invalid variable type; should be %s' % self.main_type())
                return value
            elif type == 'f':
                fn, args = rest.split(':', 1)
                if utils.get_type(obj, fn) != self.main_type():
                    raise ValidationError('invalid function type; should be %s' % self.main_type())
                return value
            raise ValidationError('invalid serialization')
        except (ValueError, IndexError, AttributeError):
            raise ValidationError('invalid serialization')

class IntegerField(BaseField):

    def main_type(self):
        return 'int'

class FloatField(BaseField):

    def main_type(self):
        return 'float'

class StringField(BaseField):

    def main_type(self):
        return 'str'

class BooleanField(BaseField):

    def main_type(self):
        return 'bool'

class InstanceField(BaseField):

    def main_type(self):
        return 'object'

class ObjectField(BaseField):
    
    def clean(self, value, model):
        BaseField.clean(self, value, model)
        s = value.split(':', 1)[1][1:-1]
        try:
            Object.objects.get(title=s)
        except Object.DoesNotExist:
            raise ValidationError('Object does not exist')
        return value

    def main_type(self):
        return 'string'

class MapField(BaseField):

    def clean(self, value, model):
        BaseField.clean(self, value, model)
        s = value.split(':', 1)[1][1:-1]
        try:
            Map.objects.get(title=s)
        except Map.DoesNotExist:
            raise ValidationError('Object does not exist')
        return value

    def main_type(self):
        return 'string'

class SpriteField(BaseField):
    def clean(self, value, model):
        BaseField.clean(self, value, model)
        s = value.split(':', 1)[1][1:-1]
        try:
            Sprite.objects.get(title=s)
        except Sprite.DoesNotExist:
            raise ValidationError('Object does not exist')
        return value

    def main_type(self):
        return 'string'

class ChoiceField(BaseField):
    '''i should just use charfield...'''

    def main_type(self):
        return 'string'

## just use instancefield
class TargetField(BaseField):

class PositionField(BaseField):
    pass


# vim: et sw=4 sts=4
