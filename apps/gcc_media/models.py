from django.db import models
from django.utils.translation import ugettext_lazy as _

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/images')

class Font(models.Model):
    font = models.FileField(upload_to='uploads/fonts')

class Sound(models.Model):
    sound = models.FileField(upload_to='uploads/sounds')

# Create your models here.
