#!/usr/bin/env python

from django.template import RequestContext
from django.shortcuts import render_to_response
from myprojects.models import Project
from basic.blog.models import Post

from django.http import HttpResponseRedirect

from django.contrib import messages

def home(request):
    return render_to_response('home.html',{'projects':Project.objects.all()[:8],
        'posts':Post.objects.all()[:3]}, context_instance = RequestContext(request))

def browse(request, slug=None):
    if category == 'latest':
        return browse_latest()
    elif category == 'popular':
        return browse_popular()
    try:
        cat = Category.objects.get(slug__iexact=slug)
        return list_detail.object_list(
                request,
                queryset=cat.project_set.all(),
                template_name='category.html'
            )
    except Category.DoesNotExist:
        messages.set_level(request, messges.ERROR)
        messages.error(request, 'That category doesn\'t exist')
    return HttpResponseRedirect('/categories/')

def categories(request):
    return fail ### WORK HERE###

# vim: et sw=4 sts=4
