#!/usr/bin/env python

import restive_js
from restive_js.ext_client import ExtClient

## setup ajax handler

ajax = ExtClient('/editor/ajax/')

def ajax_start():
    window.jQuery('#loading-icon').show()

def ajax_end():
    if not ajax.loading:
        window.jQuery('#loading-icon').hide()

ajax.listeners['start'].append(ajax_start)
ajax.listeners['end'].append(ajax_end)

import widgets
from nav import NavMan
from mediaman import MediaManager

jq = window.jQuery

class Editor:
    def __init__(self):
        self.ajax = ajax
        window.layouts['main']['items'][2]['items'][0]['buttons'][0]['handler'] = self.onProjectInfoSave
        new(window.Ext.Viewport(window.layouts['main']))
        project_name = str(window.location.hash)[1:]
        if not project_name:
            window.location = js('/create/')
        self.loader = Loader(self, project_name)
        self.nav = NavMan(self)
        self.media = MediaManager(self)

    def load(self, project, assets):
        self.project = project
        self.assets = assets
        self.populate_project_info()

    def populate_project_info(self):
        form = js.jq('#project-info form')
        js.jq('input[name=title]').val(self.project['fields']['title'])
        js.jq('input[name=version]').val(self.project['fields']['version'])
        js.jq('input[name=description]').val(self.project['fields']['description'])
        js.Ext.getCmp('project-status').setValue(self.project['fields']['status'])

    def onProjectInfoSave(self, *a):
        print 'saving pinfo!'

class Loader:
    def __init__(self, parent, project):
        self.parent = parent
        ajax.send('projects/load', {'project':project}, self.load_project)
        self.msg = widgets.NumProgressBar('Loading', 'Retrieving project data from server', 3)

    def load_project(self, data):
        models = self.organize_models(data['_models'])
        self.parent.load(**models)
        self.msg.increment()
        self.msg.setMessage('Getting Media list')
        ajax.send('media/list', {}, self.load_media)

    def load_media(self, data):
        self.msg.increment()
        self.msg.setMessage('Loading Items')
        toload = data['_models']
        self.parent.media.load(data['media_url'], toload, self.msg)
        self.msg.increment()
        self.msg.done()

    def organize_models(self, models):
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
