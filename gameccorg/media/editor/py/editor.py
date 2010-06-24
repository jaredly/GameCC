#!/usr/bin/env python

import widgets
from nav import NavMan
from mediaman import MediaManager

from sprite_editor import SpriteEditor
from object_editor import ObjectEditor
from map_editor import MapEditor

from ajax import ajax
import json

from CSS import index

jq = window.jQuery

class Editor:
    def __init__(self):
        bg = new(window.Image())
        bg.src = js('/media/editor/images/trans-bg-big.png')
        window.layouts['main']['items'][2]['items'][0]['buttons'][0]['handler'] = self.onProjectInfoSave
        new(window.Ext.Viewport(window.layouts['main']))
        self.pid = None
        project_name = str(window.location.hash)[1:]
        if not project_name:
            window.location = js('/create/')
        self.nav = NavMan(self)
        self.media = MediaManager(self)
        self.loader = Loader(self, project_name)

        self.sprites = SpriteEditor(self)
        self.objects = ObjectEditor(self)
        self.maps = MapEditor(self)

        self.editors = {'sprites': self.sprites, 'objects':self.objects, 'maps':self.maps}

    def load(self, project, assets, loader):
        self.project = project
        self.pid = project['pk']
        self.assets = assets
        self.populate_project_info()
        window.setTimeout(lambda:self.reloadFolders(loader), 100)

    def reloadFolders(self, loader):
        def cb(context):
            loader.increment()
            if loader.isDone():
                loader.done()
        self.nav.reload('sprites', cb)
        self.nav.reload('objects', cb)
        self.nav.reload('maps', cb)

    def populate_project_info(self):
        form = js.jq('#project-info form')
        js.jq('input[name=title]').val(self.project['fields']['title'])
        js.jq('input[name=version]').val(self.project['fields']['version'])
        js.jq('textarea[name=description]').val(self.project['fields']['description'])
        window.Ext.getCmp('project-status').setValue(self.project['fields']['status'])

    def attach_buttons(self):
        window.Ext.getCmp('new-sprite-button').on('click', self.new_sprite);
        window.Ext.getCmp('new-object-button').on('click', self.new_object);
        window.Ext.getCmp('new-map-button').on('click', self.new_map);

    def onProjectInfoSave(self, *a):
        print 'saving pinfo!'

class Loader:
    def __init__(self, parent, project):
        self.parent = parent
        ajax.send('project/load', {'project':project}, self.load_project)
        self.msg = widgets.NumProgressBar('Loading project', 'Retrieving project data from server', 3)

    def load_project(self, data):
        if data.has_key('error'):
            window.alert(data['error'])
            if data.has_key('action'):
                if data['action'] == 'reload':
                    window.location.reload()
                else:
                    window.location = js(data['action'])
        models = self.organize_models(data['_models'])
        self.parent.load(loader=self.msg, **models)
        self.msg.total += 3
        self.msg.increment()
        self.msg.setMessage('Getting Media list')
        ajax.send('media/list', {}, self.load_media)

    def load_media(self, data):
        self.msg.increment()
        self.msg.setMessage('Loading Items')
        toload = data['_models']
        self.parent.media.load(data['media_url'], toload, self.msg, self.finished_media)

    def finished_media(self):
        pass
        # print 'media done'

    def organize_models(self, models):
        dct = {'project':None, 'assets':{'sprites':{},'objects':{},'maps':{}}}
        for model in models:
            model = dict(model)
            if model['model'] == 'gcc_projects.project':
                dct['project'] = model
            else:
                name = '.'.join(model['model'].split('.')[1:]) + 's'
                dct['assets'][name][model['pk']] = model
                if name == 'sprites':
                    model['fields']['subimages'] = list(json.loads(model['fields']['subimages']))
        return dct

def load():
    global editor
    editor = Editor()

# vim: et sw=4 sts=4
