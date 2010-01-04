#!/usr/bin/env python

try:
    import os,sys,re
    import cgi
    import base64
    import json
    import random
    import inspect
    import traceback
except:
    print 'Content-type:text/html\n'
    print 'Unmet dependencies<br/>'
    raise

sent_header = False
debug = False
form = None

texts = {'noheader':'''
    <h1>No Header Given</h1>
    No header was sent by the server -- this is probably an error.
'''}

class StdOut:
    def __init__(self):
        self.oldout = None
        self.quiet = False
    def enable(self):
        if self == sys.stdout:return
        self.oldout = sys.stdout
        sys.stdout = self
    def disable(self):
        if self != sys.stdout:return
        sys.stdout = self.oldout
        self.oldout = None
    def write(self, txt):
        global sent_header
        if self.quiet:return
        if not txt.lower().startswith('content-type:'):
            self.oldout.write('Content-type:text/html\n\n')
            sent_header = True
            self.oldout.write(texts['noheader'])
            if debug:
                self.oldout.write('<h3>This is the first thing given:</h3><br/>'+txt)
                self.disable()
            else:
                self.quiet = True
        else:
            sent_header = True
            self.oldout.write(txt)
            self.disable()

class StdErr:
    def __init__(self):
        self.olderr = None
    def enable(self):
        if sys.stderr == self:return
        self.olderr = sys.stderr
        sys.stderr = self
    def disable(self):
        if sys.stderr != self:return
        sys.stderr = self.olderr
        self.olderr = None
    def write(self, txt):
        sys.stdout.write('An error occurred')


def enable(debugon = False):
    if debugon:
        global debug
        debug = True
    sout = StdOut()
    sout.enable()

    if debug:
        sys.stderr = sys.stdout
    else:
        serr = StdErr()
        serr.enable()
    global form
    form = cgi.FieldStorage()

def exit(data={}):
    if not data.has_key('error'):
        data['error']=''
    if not data.has_key('status'):
        data['status'] = 1
    if not sent_header:
        print 'Content-type:text/html\n'
    print json.dumps(data)
    sys.exit(0)

def die(cause = 'Invalid Arguments', **kwargs):
    if not sent_header:
        print 'Content-type:text/html\n'
    kwargs.update({'error':cause,'status':0})
    exit(kwargs)

def get_command(default=None):
    return form.getvalue('cmd',default)

import types

def getmod(key,definition):
    if not definition.has_key(key):return {}
    res = definition[key]
    if type(res) == types.ModuleType:
        return res.__dict__
    elif type(res) == dict:
        return res
    raise Exception,'Invalid definition: %s'%res

def execute(definition,default=None):

    command = get_command(default)
    if not command:
        die('No command given')

    parts = cmd.split('/')
    defn = definition
    while len(parts)>1:
        defn = getmod(parts.pop(0),defn)
    method = defn.get(parts[0],None)
    if not method:
        die('Invalid Command')


    spec = inspect.getargspec(method)
    args = spec[0]
    topass = []
    if spec[-1]:
        reqs = args[:-len(spec[-1])]
    else:
        reqs = args[:]
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

    method(*topass,**kwgs)

