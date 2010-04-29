from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings

import datetime

from colorfield.fields import ColorField

from gcc_projects.models import Project
from gcc_sprites.models import Sprite
from gcc_media.models import Font

class Object(models.Model):
    TYPE_CHOICES = (
        (1, _('Image')),
        (2, _('Text')),
        (3, _('Polygon')),
    )

    project = models.ForeignKey(Project, related_name='objects'))

    title = models.CharField(_('title'), max_length=100)
    parent = models.ForeignKey(Object, blank=True, related_name='subclasses')
    type = models.IntegerField(_('type'), choices=TYPE_CHOICES)

    #### type specific stuff ####

    ## image
    sprite = models.ForeignKey(Sprite, blank=True)

    ## text
    text = models.TextField(blank=True)
    font = models.ForeignKey(Font, blank=True)
    font_color = ColorField(blank=True)
    fint_size = models.IntegerField(blank=True)

    ## polygon
    sides = models.IntegerField(blank=True)
    length = models.IntegerField(blank=True)
    color = ColorField(blank=True)

    line_width = models.IntegerField(blank=True)
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

class Event(models.Model):
    object = models.ForeignKey(Object, related_name='events')
    type = models.CharField(max_length=100, choices=event_types)
    extra = models.CharField(max_length=100, blank=True) # for collision obj, or key name

    class Meta:
        unique_together = ('object', 'type', 'extra')

    # actions...

class Action(models.Model):
    event = models.ForeignKey(Event, related_name='actions_%(class)s')
    order = models.IntegerField(unique=True)

    class Meta:
        abstract = True

class Custom_Attr(models.Model):
    TYPE_CHOICES = (
        (1, 'int'),
        (2, 'float'),
        (3, 'string'),
        (4, 'bool'),
        (5, 'object'),
    )
    object = models.ForeignKey(Object, related_name='custom_attrs')

    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPE_CHOICES)
    sub_type = models.CharField(max_length=100)
    default_value = models.TextField()

# Create your models here.
