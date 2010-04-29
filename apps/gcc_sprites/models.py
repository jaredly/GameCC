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
    project = models.ForeignKey(Project)
    title = models.CharField(_('title'), max_length=100)
    speed = models.FloatField(_('speed'), default=1, blank=False)
    subimages = models.ManyToManyField(Image)

# Create your models here.
