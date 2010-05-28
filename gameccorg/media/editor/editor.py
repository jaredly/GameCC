#!/usr/bin/env python

import ajax
import json

import widgets
## idea; make the "json2.js" file be loaded lazily...

jq = window.jQuery

class Loader:
    def __init__(self, project):
        self.msg = widgets.NumProgressBar('Loading ' + project, 'Retrieving data from server', 1)
        ajax.post('projects/load', {'project':project}, self.onLoad)

    def onLoad(self, data):
        print data
        self.msg.increment()

def load_project(project):
    print 'loading', project
    Loader(project)

def main():
    new(window.Ext.Viewport(window.layouts['main']))

    project_name = str(window.location.hash)[1:]
    if not project_name:
        window.location = js('/create/')
    load_project(project_name)

if __name__ == '__main__':
    window.Ext.onReady(main)

# vim: et sw=4 sts=4
