'''
gcc_editor.views, by Jared Forsyth
contains the logic for displaying the editor.
'''

from django.template import RequestContext
from django.shortcuts import render_to_response
from basic.blog.models import Post
from django.views.generic import date_based, list_detail

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import messages

from gcc_projects.models import Project, Category

import os

def index(request):

    return HttpResponse(open(os.path.join(os.path.dirname(__file__), '../../gameccorg/media/editor/index.html')).read())

    return render_to_response('gcc_editor/index.html',
            {'projects':Project.objects.all()[:8],
             'posts':Post.objects.all()[:3]},
            context_instance = RequestContext(request))

