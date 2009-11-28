#!/usr/bin/python

'''
compile_game.py
'''

import os,sys,re,math
import myjson as json
import glob
import random as Random
import string

import drupal
import multivalueable

from utils import die,exit

sys.stderr = sys.stdout

class InvalidArgumentException(Exception):pass
class ArgumentException(Exception):pass

def execute(x):
  res = os.popen3(x).read()
  print res[1].read()
  print res[2].read()

class Asset:
  base = ''
  first=None
  sorted = sorted
  def __init__(self,parent,name,info=None):
    self.name = name
    self.parent = parent
    self.info = info
    self.raw = str(info).replace('False','false').replace("True",'true').replace('None','null')
    if not info:
      self.load()
    
  @classmethod
  def outputAll(cls,parent,otype):
    atype = cls.base.split('/')[-1]
    return '\n'.join(asset.output(otype) for name,asset in cls.sorted(parent.assets[atype].items()))
    
  @classmethod
  def outputMAll(cls,parent,otype):
    atype = cls.base.split('/')[-1]
    return '\n'.join(list(asset.outputMore(otype) for name,asset in cls.sorted(list(parent.assets[atype].items()))))
  
  def load():pass
  
  #def load(self):
   # self.info = 
    #self.raw = open(os.path.join(self.parent.base,self.base,self.name + '.info')).read().strip().replace('\r\n','\n')
    #true=True;false=False;null=None
    #self.info = eval(self.raw)
    
  def output(self, otype):
    if otype == 'haxe':
      return self._output_haxe()
    elif otype == 'python':
      return self._output_python()
    else: raise NotImplemented,"invlaid output type"
  def _output_haxe(self):
    self.raw = re.sub('"(\w+)"\s*:',(lambda x:x.groups()[0]+' :'),self.raw)
    self.raw = re.sub("'(\w+)'\s*:",(lambda x:x.groups()[0]+' :'),self.raw)
    return ''
  def _output_python(self):
    self.raw = self.raw.replace('false','False').replace('true','True').replace('null','None')
    return ''
  
  def outputMore(self, otype):
    return ''

class PluginAsset(Asset):
  base = '../plugins'
  sprite_template = {'python':'''
class BaseObject(Object):
%(functions)s
''','haxe':'''
class BaseObject extends ImageSprite {
%(functions)s
}
'''}
  def __init__(self,parent,name,info=None):
    Asset.__init__(self,parent,name,info)
    if self.info['type'] == 'conditional':
      self.info['inputs']['not'] = 'not'
  
  @classmethod
  def outputAll(cls,parent,otype):
    return ''
    
  @classmethod
  def outputMAll(cls,parent,otype):
    functions = []
    for name,plugin in parent.assets['plugins'].items():
      functions.append('  '+plugin.getFunction(otype).replace('\n','\n  ')+'\n')
    return cls.sprite_template[otype]%{'functions':''.join(functions)}
  
  def load(self):
    self.raw = open(os.path.join(self.parent.base,'../plugins',self.name,self.name + '.info')).read().strip().replace('\r\n','\n')
    true=True;false=False;null=None
    self.info = eval(self.raw)
    sys.path.append('../plugins/'+self.name+'/')
    self.module = __import__(self.name)
  
  def getFunction(self,otype):
    base = os.path.join(self.parent.base,self.base,self.name,self.name)
    if otype == 'python':
      if os.path.exists(base+'.inc.py'):
        return open(base+'.inc.py').read().strip()
    elif otype == 'haxe':
      if os.path.exists(base+'.inc.hx'):
        return open(base+'.inc.hx').read().strip()
    return ''
  
  ## fix outputs
  def output(self, data, otype, event, args, object):
    for k,v in data.items():
      if k == 'disabled':continue
      if not self.info['inputs'].has_key(k):
        raise Exception,'invalid plugin input data name "%s" for plugin "%s" and data"%s"'%(k,self.info['name'],data)
      input_type = self.info['inputs'][k]
      
      if input_type == 'conditional':
        cond = data[k]
        data[k] = self.parent.assets['plugins'][data[k]['name']].output(data[k]['data'],otype, event, args, object)
      elif input_type == 'speed':
        data[k] = '%s,%s'%(multivalueable.convert[v[0]](v[1],otype,self), {'haxe':['false','true'],'python':[False,True]}[otype][v[0] == 'percent'])
      else:
        ## for percentage --
        data[k] = multivalueable.convert[v[0]](v[1],otype,self)
    if not data.has_key('appliesto'):
      data['appliesto']='self'
    if data['appliesto'] == 'self':
      data['appliesto'] = {'python':'self','haxe':'this'}[otype]
    data['_parent'] = object.info['parent']
    data['_event'] = event
    data['_args'] = args
    #if not hasattr(self.module,'output'):
    #  print self.module,self.name
    return self.module.output(data, otype)

class SimpleAsset(Asset):
  def _output_haxe(self):
    Asset._output_haxe(self)
    return '    ' + self.base + '.set("%s",%s);'%(self.info['name'],self.raw)
  def _output_python(self):
    Asset._output_python(self)
    return '    ' + self.base + '["%s"] = %s'%(self.info['name'],self.raw)

class ImageAsset(SimpleAsset):
  base = 'images'
  @classmethod
  def outputMAll(cls,parent,otype):
    atype = cls.base.split('/')[-1]
    if not parent.assets[atype].items():return ''
    return parent.assets[atype].items()[0][1].outputMore(otype)
    
  def outputMore(self, otype):
    res = set()
    for name,img in self.parent.assets['images'].items():
      res |= set(img.info['subimages'])
    return str(list(res))

class MapAsset(SimpleAsset):
  base = 'maps'
  first = None
  @classmethod
  def outputMAll(cls,parent,otype):
    atype = cls.base.split('/')[-1]
    if not parent.assets[atype].items():return ''
    return parent.assets[atype].items()[0][1].outputMore(otype)
  def outputMore(self, otype):
    return self.first

class ObjectAsset(SimpleAsset):
  base = 'objects'
  defaultparent = 'BaseObject'
  class_template = {'haxe':'''
class %(name)s extends %(parent)s {
  // any class variables (when I decide to include that) will go here
  public override function new(parent:Game, x:Float, y:Float) {
    if (this.image==null)
      this.image = "%(image)s";
    super(parent, x, y);
    this.collisions = %(collisions)s;
  }
  %(functions)s
}
''',
                    'python':'''
class %(name)s(%(parent)s):
  image = "%(image)s"
  collisions = %(collisions)s
  # any class variables (when I decide to include that) will go here
  def __init__(self, parent, x, y):
    %(parent)s.__init__(self, parent, x, y)
  
  def keyevent(self, type, key):
    'event handling'
    if type == KEYDOWN:
      'check keypress'
      %(keypress)s
    elif type == KEYUP:
      'check keyrelease'
      %(keyrelease)s
  
  def _check_keydown(self):
      keys = self.parent.keys()
      %(keydown)s
  
  %(functions)s
'''}
  func_template = {'haxe':'''
  public %(override)s function %(event)s(%(args)s){
    %(actions)s
    //super(%(args)s);
  }
  ''',
                   'python':'''
  def %(event)s(self, %(args)s):
    %(actions)s
    #super(%(args)s);
  '''}
  @classmethod
  def sorted(cls,objectlist):
    ## deal w/ parentage -- parents need to be outputted first.
    for n,o in objectlist:
      if o.parent != 'BaseObject':break
    else:
      return objectlist
    def gi(n):
      return [o[0] for o in objectlist].index(n)
    
    while 1:
      for i,(n,o) in enumerate(objectlist):
        if not o.info['parent'] or o.info['parent'] == 'BaseObject':continue
        pi = gi(o.info['parent'])
        if pi>i:
          objectlist.insert(0,objectlist.pop(pi))
          break
      else:
        break
    return objectlist
  
  def _output_haxe(self):
    Asset._output_haxe(self)
    return '    ' + self.base + '.set("%s",%s);'%(self.info['name'],self.info['name'])
  def _output_python(self):
    Asset._output_python(self)
    return '    ' + self.base + '["%s"] = %s'%(self.info['name'],self.info['name'])
    
  def makeKey(self, event):
    plain = '_'.join(event.split('_')[2:])
    if event.startswith('key_down'):
      return 'if keys[%s]: self.%s()\n      '%(multivalueable.reversed_keys['python'][plain], event)
    else:
      return 'if key == %s: self.%s()\n      '%(multivalueable.reversed_keys['python'][plain], event)

  def outputMore(self,otype):
    if not self.info.get('parent',None):
      self.info['parent'] = self.defaultparent
    self.info['name'] = self.info['name'].replace(' ','_')
    functions = []
    collisions = []
    self.info['keydown'] = ''
    self.info['keypress'] = ''
    self.info['keyrelease'] = ''
    for event in self.info['events']:
      if event.startswith('collide_'):
        collisions.append(event.split('_',1)[1])
      elif event.startswith('key_down'):
        self.info['keydown'] += self.makeKey(event)
      elif event.startswith('key_press'):
        self.info['keypress'] += self.makeKey(event)
      elif event.startswith('key_release'):
        self.info['keyrelease'] += self.makeKey(event)
      #try:
      functions.append(self._make_function(event,self.info['events'][event], otype))
      #except Exception,e:
      #die( 'Error in making the event "%s" for object "%s": %s; %s %s'%(event,self.name,e,otype,self.info['events'][event]) )
        
    if self.info['parent'] != 'BaseObject':
      self.info['keydown'] += self.parent.assets['objects'][self.info['parent']].info['keydown']
      self.info['keypress'] += self.parent.assets['objects'][self.info['parent']].info['keypress']
      self.info['keyrelease'] += self.parent.assets['objects'][self.info['parent']].info['keyrelease']
      collisions += self.parent.assets['objects'][self.info['parent']].info['rawcollisions']
    self.info['functions'] = ''.join(functions)
    self.info['collisions'] = '[]'
    self.info['rawcollisions'] = collisions
    if collisions:
      self.info['collisions'] = '["'+'","'.join(collisions)+'"]'
    elif otype=='haxe':
      self.info['collisions'] = 'new Array<String>()';
    
    return self.class_template[otype]%self.info

  def _make_function(self,event,actions,otype):
    data = {'args':'','args2':''}
    ## make this better, kindof a hack...
    if self.info['parent']!=self.defaultparent:
      pevents = self.parent.assets['objects'][self.info['parent']].info['events']
    else:
      pevents = {}
    if event.startswith('collide_') and event not in pevents:
      data['override']=''
    else:
      data['override']='override'
    
    if event.startswith('mouse'):
      data['args'] = 'e:flash.events.MouseEvent'
      data['args2'] = 'e'
    elif event.startswith('collide'):
      data['args'] = 'other:BaseObject'
      data['args2'] = 'other'
    
    if otype == 'python':
      data['args'] = data['args2']
    
    data['event'] = event
    data['actions'] = []
    indent = 0
    last = None
    
    block_start = 'if','and','or','else','elif','while','with','repeat','else','elif'
    block_end   = 'else','elif','endif'
    comments = {'python':'## ','haxe':'// '}
    
    for action in actions:
      if action[1].get('disabled',False):
        data['actions'].append(comments[otype]+' '*indent + self.parent.assets['plugins'][action[0]].output(action[1],otype,event,data['args2'],self).replace('\n','\n'+comments[otype]+' '*indent))
        continue
      if action[0] in block_end:
        if last in block_start and otype=='python':
          data['actions'][-1] += 'pass'
        indent -= 2
      data['actions'].append(' '*indent + self.parent.assets['plugins'][action[0]].output(action[1],otype,event,data['args2'],self).replace('\n','\n'+' '*indent))
      if action[0] in block_start:
        indent += 2
      last = action[0]
        
    if not data['actions'] and otype == 'python':
      data['actions'] = ['pass']
    data['actions'] = '\n    '.join(data['actions'])
    return self.func_template[otype]%data

class Compiler:
  templates = {'haxe':open('../data/haxe_template.hx').read(),
               'python':open('../data/haxe_template.py').read()}
  def __init__(self,project):
    self.project = project
    self.base = ''
    self.assets = {'plugins':{},'images':{},'objects':{},'maps':{}}
    self.assetTypes = {'plugins':PluginAsset,'images':ImageAsset,'objects':ObjectAsset,'maps':MapAsset}
    
    for atype,aclass in self.assetTypes.items():
      self.load_assets(atype,aclass)
    
    self.width = max(m.info['width'] for m in self.assets['maps'].values())
    self.height = max(m.info['height'] for m in self.assets['maps'].values())
    
  def genName(self):
    name = ''.join(Random.choice(string.ascii_lowercase) for x in range(10)).title()
    return name
  
  def load_assets(self,atype,aclass):
    if atype == 'plugins':
      for path in glob.glob(os.path.join(self.base,aclass.base,'*.info')) + glob.glob(os.path.join(self.base,aclass.base,'*','*.info')):
        name = path.split('/')[-1].split('.')[0]
        self.assets[atype][name] = aclass(self,name,None)
    else:
      for item in drupal.db.find_dict(atype,order='aorder'):
        name = item['name']
        del item['uid']
        del item['pid']
        del item['tags']
        del item['aorder']
        del item['folder']
        if not aclass.first:
          aclass.first = name
        self.assets[atype][name] = aclass(self,name,item)

  def compile(self, otype, save=True):
    exts = {'python':'.py','haxe':'.hx'}
    thename = self.genName()
    
    if not thename:
      thename = self.genName()
    data = {'name':thename}
    for name, atype in self.assetTypes.items():
      data[name] = atype.outputAll(self,otype)
    for name, atype in self.assetTypes.items():
      data[name+'_more'] = atype.outputMAll(self,otype)
    if otype == 'haxe':
      op = data['plugins_more']
      data['plugins_more'] = ''
    data['otype'] = otype
    data['width'] = self.width
    data['height'] = self.height
    text = self.templates[otype]%data
    
    if not save:return text,data
    
    open(thename+exts[otype],'w').write(text)
    if otype=='haxe':
      open('game/BaseObject.hx','w').write('''package game;
import game.Game;
import game.Sprite;
import game.Vector;
import flash.geom.Point;
import flash.events.Event;
import flash.display.BitmapData;
import flash.display.Loader;
import flash.net.URLRequest;
import flash.ui.Keyboard;
'''+op)
    return thename
    
import sys
if __name__=='__main__':
  if len(sys.argv)>=2:
    print Compiler(sys.argv[1]).compile('python')
  else:print 'no project given. exiting'
#if __name__=='__main__':
#  Compiler('temp','MGame').compile('flash')
#  os.system('./compile.sh MGame.hx MGame && firefox MGame.hx.html')
    
