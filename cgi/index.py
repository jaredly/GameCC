#!/usr/bin/env python

import cgitools
from cgitools import form, die
cgitools.enable(True)

import project
import asset
import objects
import images
import maps
import viewer
import traceback
import drupal

structure = {
    'project':project,
    'objects':objects,
    'images':images,
    'maps':maps,
    'viewer':viewer,
    'login':drupal.login
}

if __name__=='__main__':
    command = cgitools.get_command()
    if not drupal.login():
        if command.startswith('viewer'):
            if not drupal.altlogin(form):
                die('Not logged in')
        if command != 'login':
            die('Not logged in')
    if form.has_key('project'):
        drupal.getpid(form['project'].value)
        if drupal.pid is None and command not in project.noproject:
            die('Invalid project name')
    try:
        cgitools.execute(structure)
    except SystemExit:
        pass
    except:
        die(traceback.format_exc().split('\n')[-2],traceback=traceback.format_exc())


