#!/usr/bin/env python

import os,sys,re
import cgi
import base64
import myjson as json
import random

sys.stderr = sys.stdout
form = cgi.FieldStorage()

import project
import asset
import objects
import images
import maps
import viewer

import subprocess

send_header = False

from utils import exit,die,drupal

import inspect
import traceback


def execute_command(cmd):
  prefill = []
  if '/' in cmd:
    mod,func = cmd.split('/')
    if not mod in ('objects','images','maps','project','viewer'):
      raise die("invalid command")
    if mod not in ('project','viewer') and func in asset.__dict__.keys():
      command = asset.__dict__[func]
      prefill = [mod]
    else:
      module = globals()[mod]
      command = module.__dict__[func]
  else:
    die('Invalid command')
  
  spec = inspect.getargspec(command)
  args = spec[0]
  topass = []
  if spec[-1]:
    reqs = args[len(prefill):-len(spec[-1])]
  else:
    reqs = args[len(prefill):]
  for arg in reqs:
    if not form.has_key(arg):
      die("Arg not provided %s"%arg)
    if form[arg].filename:#is file
      topass.append(form[arg])
    else:
      topass.append(form[arg].value)
  kwgs = {}
  if spec[-1]:
    nonreqs = args[-len(spec[-1]):]
  else:
    nonreqs = []
  for arg in nonreqs:
    if form.has_key(arg):
      if form[arg].filename:#is file
        kwgs[arg] = form[arg]
      else:
        kwgs[arg] = form[arg].value
  if not args:command()
  command(*(prefill+topass),**kwgs)

if __name__=='__main__':
  print 'Content-type:text/html\n'
  if not form.has_key('cmd'):
    die('Missing command argument')
  cmd = form['cmd'].value
  send_header = True
  
  drupal.login()
  if cmd.startswith('viewer') and not drupal.loggedin:
    drupal.altlogin(form)
  
  if not drupal.loggedin:
    die('Not logged in')
  if form.has_key('project'):
    drupal.getpid(form['project'].value)
    if drupal.pid is None and not cmd.startswith('project/'):
      die('Invalid Project Name')
  try:
    execute_command(cmd)
  except SystemExit:
    pass
  except :
    die(traceback.format_exc().split('\n')[-2],traceback=traceback.format_exc())

