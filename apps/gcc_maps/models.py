from django.db import models
from django.utils.translation import ugettext_lazy as _

from colorfield.fields import ColorField

from gcc_projects.models import Project
from gcc_objects.models import Object
from gcc_media.models import Image, Sound

class Map(models.Model):
    project = models.ForeignKey(Project, related_name='maps')
    order = models.IntegerField(_('order'))

    title = models.CharField(_('title'), max_length=100)

    width = models.IntegerField(_('width'), default=600)
    height = models.IntegerField(_('height'), default=600)

    grid_size = models.IntegerField(_('grid size'), default=50)

    background = models.ForeignKey(Image, blank=True)
    background_color = ColorField(default='#FFF')
    background_music = models.ForeignKey(Sound, blank=True)

    class Meta:
        unique_together = ('project', 'order')

class Layer(models.Model):
    map = models.ForeignKey(Map, related_name='layers')
    order = models.IntegerField(_('order'))

    title = models.CharField(_('title'), max_length=100)
    visible = models.BooleanField(_('visible'), default=True)
    
    class Meta:
        unique_together = ('map', 'order')

class Instance(models.Model):
    '''an instance of an object, placed on a map with a specified scale and
    rotation.
    '''
    layer = models.ForeignKey(Layer, related_name='instances')
    rotation = models.FloatField(_('rotation'), default=0.0)
    scale = models.FloatField(_('scale'), default=1.0)

    x = models.IntegerField(_('x position'))
    y = models.IntegerField(_('y position'))

    object = models.ForeignKey(Object)

class Camera(models.Model):
    '''a window to look at a map. can follow an instance or not
    '''
    map = models.ForeignKey(Map, related_name='views')
    x = models.IntegerField(_('x position'))
    y = models.IntegerField(_('y position'))
    width = models.IntegerField(_('width'), default=600)
    height = models.IntegerField(_('height'), default=600)

    rotation = models.FloatField(_('rotation'), default=0.0)
    scale = models.FloatField(_('scale'), default=1.0)

# Create your models here.
