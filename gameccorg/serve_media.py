'''This is a drop in module to manage serving static files in a development context'''
import os
import mimetypes
from django.conf import settings
from django.shortcuts import Http404
from django.http import HttpResponse
from django.views.static import directory_index
from django.utils.importlib import import_module

import imp

from runpy import run_module

def get_path(path, root):
    short = path.split('/')[0]
    for app in settings.INSTALLED_APPS:
        if app.split('.')[-1] != short:continue
        app_dir = os.path.dirname(import_module(app).__file__)
        break
    else:
        if root:
            return os.path.join(root, path)
        return None
    return os.path.join(app_dir, 'media', path.split('/',1)[1])

def serve_all(request, path, document_root=None):
    """
    This view serves static media and directory indexes for a django application. It should
    only be used in development, media should be provided directly by a web server in production.
    
    This view assumes a django application stores its media in app/media (which is very common) and
    the file is referred to in the templates by the last part of a django app path. e.g. As in
    django.contrib.admin -> 'admin'.
    
    First we check if the media is a request in an application directory; if so we attempt to serve
    it from there. Then we attempt to provide the document from the document_root parameter (if
    provided).

    To use this view you should add something like the following to urls.py:
    if settings.DEBUG:
        urlpatterns += (r'^media/(?P<path>.*)$', 'site.media.serve_apps', {'document_root' : settings.MEDIA_ROOT})
        
    You can then have the admin media files served by setting
    ADMIN_MEDIA_PREFIX = '/media/admin/'
    """
    
    abspath = get_path(path, document_root) #find_abspath(path, document_root) or ''
    if not os.path.exists(abspath):
        raise Http404("No media found for path %s (tried '%s'), root: %s" % (path, abspath,document_root))
    if os.path.isdir(abspath):
        # To make the template work a directory must have a trailing slash in the url
        # The one exception is when path == /
        if not path.endswith('/') and path:
            raise Http404("This path is a directory. Add a trailing slash to view index")
        return directory_index(path[:-1], abspath)
    
    mimetype = mimetypes.guess_type(abspath)[0] or 'application/octet-stream'
    contents = open(abspath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Content-Length"] = len(contents)
    return response
