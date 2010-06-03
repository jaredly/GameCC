# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf

from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.core import serializers

from gcc_media.models import Image

from gameccorg.decorators import my_login_required

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image']

@my_login_required(None, message='''You must be logged in to create and edit projects. Please login below or `register an account </registration/new_user/>`_''')
def upload(request, ftype):
    form = {'image':ImageForm}.get(ftype, None)
    if not form:
        return HttpResponse('Sorry, uploading %s is not yet supported' % ftype)
    if request.method == 'POST':
        myform = form(request.POST, request.FILES)
        if myform.is_valid():
            model = myform.save(commit=False)
            model.author = request.user
            model.save()
            return HttpResponse(serializers.serialize('json', [model], use_natural_keys=True))
    else:
        myform = form()
    return render_to_response('gcc_media/upload.html',
            {'upload_form': myform},
            context_instance = RequestContext(request))

