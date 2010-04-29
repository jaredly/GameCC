from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings

import datetime

class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'gcc_projects_categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('project_category_detail', None, {'slug': self.slug})

class Project(models.Model):
    '''The base model, used to aggregate images, objects and maps into a
    cohesive whole. Has an author and a state of completion.
    '''
    STATUS_CHOICES = (
        (1, _('Pre-Alpha')),
        (2, _('Alpha')),
        (3, _('Beta')),
        (4, _('Release'))
    )
    author = models.ForeignKey(User)
    
    title = models.CharField(_('title'), max_length=100)
    slug  = models.SlugField(_('slug'))
    version = models.FloatField(_('version'))
    categories = models.ManyToManyField(Category, blank=True)
    
    description = models.TextField(_('description'), blank=True, help_text=_('Describe your project'))

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        db_table = 'gcc_projects'
        ordering = ('-created',)
        get_latest_by = 'created'
        unique_together = (('author', 'slug'), ('author', 'title'))

    def __unicode__(self):
        return u'%s' % self.title
    
    @permalink
    def get_absolute_url(self):
        return ('project_detail', None, {
            'author': self.author.name,
            'title': self.title
        })

