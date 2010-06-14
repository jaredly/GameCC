#!/usr/bin/env python

from django.forms import ModelForm

from gcc_projects.models import Project

class NewProject(ModelForm):
    class Meta:
        model = Project
        exclude = 'author', 'status', 'slug', 'sprite_folder', 'object_folder', 'map_folder'

# vim: et sw=4 sts=4
