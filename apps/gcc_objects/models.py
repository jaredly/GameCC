from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.db.models.fields import FieldDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings

import datetime

from colorfield.fields import ColorField

from gcc_projects.models import Asset
from gcc_sprites.models import Sprite
from gcc_media.models import Font

class Object(Asset):
    '''Object - handles the main logic of an object in a game. Has the three
    types "Image", "Text", and "Polygon" for maximum flexibility in display.
    Is associated w/ a project, and has events with actions.
    '''
    TYPE_CHOICES = (
        ('image', _('Image')),
        ('text', _('Text')),
        ('polygon', _('Polygon')),
    )

    ## parent from Asset

    title = models.CharField(_('title'), max_length=100)

    parent = models.ForeignKey('self', null=True, related_name='subclasses')
    solid = models.BooleanField(_('solid'), default=False)
    persistent = models.BooleanField(_('persistent'), default=False)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)

    #### type specific stuff ####

    ## image
    sprite = models.ForeignKey(Sprite, null=True)

    ## text
    text = models.TextField(blank=True)
    font = models.ForeignKey(Font, null=True)
    font_color = ColorField(blank=True)
    font_size = models.IntegerField(null=True)

    ## polygon
    sides = models.IntegerField(null=True)
    length = models.IntegerField(null=True)
    color = ColorField(blank=True)

    line_width = models.IntegerField(null=True)
    line_color = ColorField(blank=True)

    #### other ####

    # events...

    # custom_attrs...

event_types = '''\
create
created
destroy
collide
timer
step
draw
move
mouse_up
mouse_down
mouse_move
key_down
key_press
key_release
off_of_map
map_start
map_end
game_start
game_end\
'''.split('\n')

event_vbls = {
    'created':{'creator':'object'},
    'collide':{'other':'object'},
#    'key_down':{'key':'int'},
#    'key_press':{'key':'int'},
#    'key_release':{'key':'int'},
}

class Event(models.Model):
    object = models.ForeignKey(Object, related_name='events')
    type = models.CharField(max_length=100,
            choices=tuple((a,a) for a in event_types))
    extra = models.CharField(max_length=100, blank=True) # for collision obj, or key name

    class Meta:
        unique_together = ('object', 'type', 'extra')

    # actions...

class Action(models.Model):
    event = models.ForeignKey(Event, related_name='actions_%(class)s')
    order = models.IntegerField(unique=True)

    target = 'self'
    ICON = None
    TYPE = None
    DEPENDS = ()
    DEFAULT_LINES = {
        'python':'%s.%s(%s)\n',
        'haxe':'%s.%s(%s);\n',
        'javascript':'%s.%s(%s);\n',
    }
    LINES = None
    METHODS = ()
    ARG_ORDER = ()
    EVENTS = ()
    GAME_METHODS = ()
    INIT = None
    GAME_INIT = None

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'Generic Action'

    def export(self, lang):
        if LINES:
            return self.export_line(lang)
        name = self.__class__.__name__.lower()
        args = ', '.join(utils.export(getattr(self, arg), lang) \
                         for arg in self.ARG_ORDER)
        return self.DEFAULT_LINES[lang] % (self.get_target(lang), name, args)
    
    def export_line(self, lang):
        dct = {}
        for field in self._meta.fields:
            value = getattr(self, field.attname)
            # what was this line to be?
            #if not value.
            dct[field.attname] = utils.export(value, lang)
        return self.LINES[lang] % dct

    def get_target(self, lang):
        try:
            field = self._meta.get_field_by_name('target')[0]
        except FieldDoesNotExist:
            target = self.target
        else:
            return field.export(lang)
        if lang == 'haxe' and self.target == 'self':
            return 'this'

class Custom_Attr(models.Model):
    TYPE_CHOICES = (
        ('int', 'int'),
        ('float', 'float'),
        ('string', 'string'),
        ('bool', 'bool'),
        ('object', 'object'),
    )
    object = models.ForeignKey(Object, related_name='custom_attrs')

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    sub_type = models.CharField(max_length=100)
    default_value = models.TextField()

# Create your models here.
