from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings

import datetime
import tagging
from tagging.fields import TagField

from gcc_projects.models import Project
from gcc_media.models import Image

class Sprite(models.Model):
    '''handles subimages and collision masks
    '''
    COLLISION_TYPES = (
        (1, _('Circle')),
        (2, _('Rectangle')),
        (3, _('Polygon')),
        (4, _('Oval')),
        (5, _('Exact')),
    )
    project = models.ForeignKey(Project, related_name='sprites')
    title = models.CharField(_('title'), max_length=100)
    speed = models.FloatField(_('speed'), default=1, blank=False)
    subimages = models.ManyToManyField(Image)

    collision_type = models.IntegerField(_('collision type'), default=1, choices = COLLISION_TYPES)
    collision_attrs = models.TextField() # cop out...

# Create your models here.
