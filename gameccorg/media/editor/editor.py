#!/usr/bin/env python

import ajax
import json

import widgets

## idea; make the "json2.js" file be loaded lazily...

jq = window.jQuery

class Loader:
    def __init__(self, parent, project):
        self.parent = parent
        ajax.post('projects/load', {'project':project}, self.load_project)
        self.msg = widgets.NumProgressBar('Loading', 'Retrieving project data from server', 3)

    def load_project(self, data):
        models = self.organize_models(data['_models'])
        self.parent.onLoad(**models)
        self.msg.increment()
        ajax.post('media/list', {}, self.load_media)

    def load_media(self, data):
        pass

    def organize_models(self, text):
        that = json.loads(text)
        models = list(that)
        dct = {'project':None, 'assets':{'sprites':{},'objects':{},'maps':{}}}
        for model in models:
            model = dict(model)
            if model['model'] == 'gcc_projects.project':
                dct['project'] = model
            else:
                name = model['model'].split('.')[1:] + 's'
                dct['assets'][name][model['title']] = model
        return dct

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


def load():
    global editor
    editor = Editor()

# vim: et sw=4 sts=4
