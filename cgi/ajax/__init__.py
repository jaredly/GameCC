import cgitools
from cgitools import form, die
cgitools.enable(True)

import traceback
import project
import objects
import images
import viewer
import drupal
import asset
import maps

import sys

#good: Jan 4

structure = {
    'project':project,
    'objects':objects,
    'images':images,
    'maps':maps,
    'viewer':viewer,
    'login':drupal.login
}

import cProfile

def main():
    command = cgitools.get_command()
    if not drupal.login():
        if command.startswith('viewer'):
            if not drupal.altlogin(form):
                die('Not logged in')
        if command != 'login':
            die('Not logged in')
    if form.has_key('pid'):
        drupal.pid = int(form['pid'].value)
        if drupal.pid is None and command not in project.noproject:
            die('Invalid project name')
    try:
        cProfile.run('cgitools.execute(structure)','profiles/'+command.replace('/','_')+'.prof')
    except SystemExit:
        pass
    except:
        die(traceback.format_exc().split('\n')[-2],traceback=traceback.format_exc())
