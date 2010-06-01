#!/usr/bin/env python

import restive_js
from restive_js.client import Client

ajax = Client('/editor/ajax/')

import json

import widgets

## idea; make the "json2.js" file be loaded lazily...

jq = window.jQuery

class Editor:
    def __init__(self):
        new(window.Ext.Viewport(window.layouts['main']))
        project_name = str(window.location.hash)[1:]
        if not project_name:
            window.location = js('/create/')
        self.loader = Loader(self, project_name)

    def onLoad(self, project, assets):
        self.project = project
        self.assets = assets

class Loader:
    def __init__(self, parent, project):
        self.parent = parent
        ajax.send('projects/load', {'project':project}, self.load_project)
        self.msg = widgets.NumProgressBar('Loading', 'Retrieving project data from server', 3)

    def load_project(self, data):
        models = self.organize_models(data['_models'])
        self.parent.onLoad(**models)
        self.msg.increment()
        self.msg.setMessage('Getting Media list')
        ajax.send('media/list', {}, self.load_media)

    def load_media(self, data):
        self.msg.increment()
        self.msg.setMessage('Loading Items')
        toload = data['_models']
        if len(toload):
            print 'have media!!', data
            fail
        self.msg.increment()
        self.msg.done()

    def organize_models(self, models):
        models = list(models)
        dct = {'project':None, 'assets':{'sprites':{},'objects':{},'maps':{}}}
        for model in models:
            model = dict(model)
            if model['model'] == 'gcc_projects.project':
                dct['project'] = model
            else:
                name = model['model'].split('.')[1:] + 's'
                dct['assets'][name][model['title']] = model
        return dct


def load():
    global editor
    editor = Editor()

# vim: et sw=4 sts=4
