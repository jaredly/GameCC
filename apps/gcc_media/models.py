from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/images')
    author = models.ForeignKey(User, related_name='gcc_images')

class Font(models.Model):
    font = models.FileField(upload_to='uploads/fonts')
    author = models.ForeignKey(User, related_name='gcc_fonts')

class Sound(models.Model):
    sound = models.FileField(upload_to='uploads/sounds')
    author = models.ForeignKey(User, related_name='gcc_sounds')

# Create your models here.
