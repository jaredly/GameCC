#!/usr/bin/env python

from django.template import RequestContext
from django.shortcuts import render_to_response
from myprojects.models import Project
from basic.blog.models import Post
from django.views.generic import date_based, list_detail
## my login_required
from decorators import my_login_required

from django.http import HttpResponseRedirect

from django.contrib import messages

from gcc_projects.models import Project, Category

def home(request):
    return render_to_response('home.html',{
            'projects':Project.objects.all()[:8],
            'posts':Post.objects.all()[:3]
        }, context_instance = RequestContext(request))

def create(request):
    if not request.user.is_authenticated():
        return render_to_response('login.html', {'to_url':'/create/'},
                context_instance=RequestContext(request))
    return render_to_response('create.html', {
            'my_projects':request.user.my_projects,
        }, context_instance=RequestContext(request))
create = my_login_required(create, message='''You must be logged in to create and edit projects. Please login below or `register an account </registration/new_user/>`_''')

def browse(request, category=None):
    if not category: category = 'latest'
    if category == 'latest':
        return list_detail.object_list(
                request,
                queryset=Project.objects.all().order_by('-modified'),
                template_name='gamecc/project_list.html',
            )
    elif category == 'popular':
        return list_detail.object_list(
                request,
                queryset=Project.objects.all().order_by('-modified'),
                template_name='gamecc/project_list.html',
            )
    elif category == 'categories':
        return list_detail.object_list(
                request,
                queryset=Category.objects.all(),
                template_name='gamecc/categories.html',
            )
    else:
        try:
            cat = Category.objects.get(slug__iexact=category)
            return list_detail.object_list(
                    request,
                    queryset=cat.project_set,
                    template_name='gamecc/category.html'
                )
        except Category.DoesNotExist:
            messages.set_level(request, messges.ERROR)
            messages.error(request, 'That category doesn\'t exist')
        return HttpResponseRedirect('/browse/categories/')

# vim: et sw=4 sts=4
