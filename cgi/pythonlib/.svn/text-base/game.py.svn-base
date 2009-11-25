import rabbyt
import pygame
from pygame.locals import *
import inspect

import fixrabbyt
import pygame_font
import math

class Object(object):
  _imagename = None
  
  _get_vspeed = lambda s:s._velocity.y
  _set_vspeed = lambda s, x:setattr(s._velocity,'y',x)
  _get_hspeed = lambda s:s._velocity.x
  _set_hspeed = lambda s, x:setattr(s._velocity,'x',x)
  _get_x      = lambda s:s._sprite.x
  _set_x      = lambda s, x:setattr(s._sprite,'x',x)
  ## flip to be the same as all traditional surfaces
  _get_y      = lambda s:-s._sprite.y
  _set_y      = lambda s, x:setattr(s._sprite,'y',-x)
  _get_direction = lambda s:s._velocity.degrees
  _set_direction = lambda s, x:setattr(s._velocity,'degrees',x)
  _get_speed  = lambda s:s._velocity.speed
  _set_speed  = lambda s, x:setattr(s._velocity,'speed',x)
  _get_gdirection = lambda s:s._gravity.degrees
  _set_gdirection = lambda s, x:setattr(s._gravity,'degrees',x)
  _get_gspeed  = lambda s:s._gravity.speed
  _set_gspeed  = lambda s, x:setattr(s._gravity,'speed',x)
  _get_image   = lambda s:s._imagename
  _set_image   = lambda s, x:setattr(s,'_imagename',x) and self._updateimage()
  _get_opacity = lambda s:s._sprite.alpha
  _set_opacity = lambda s, x:setattr(s._sprite,'alpha',x)
  _get_rotation = lambda s:s._sprite.rot
  _set_rotation = lambda s, x:setattr(s._sprite,'rot',x)
  
  for attr in ['vspeed','hspeed','x','y','speed','direction','gspeed','gdirection','image','rotation']:
    locals()[attr] = property(locals()['_get_'+attr],locals()['_set_'+attr])
  
  def __init__(self, parent, x, y):
    self.parent  = parent
    self.image = self._imagename
    self._image   = parent.images[self.image]
    self._sprite  = rabbyt.Sprite(self._image['subimages'][0])
    
    self.imagepos  = 0
    self.imagespeed = 1
    self.x = x
    self.y = y
    self._velocity  = Vector(0,0)
    self._gravity = Vector(0,0)
    
    self.create()
  
  def render(self, *a, **b):
    self._sprite.render(*a,**b)
  
  def _updateimage(self):
    self._image = self.parent.images[self.image]
  
  def event(self,*a):pass
  def create(self):pass
  
  def _step(self):
    self._velocity += self._gravity
    self.x += self._velocity.x
    self.y += self._velocity.y
    self.imagepos += self.imagespeed
    if int(self.imagepos)>=len(self._image['subimages']):
      self.imagepos = 0
    self._sprite.texture = self._image['subimages'][int(self.imagepos)]
    self._check_keys()
    self.step()
  
  def step(self):pass
  
  def _check_keys(self):pass
  
  def limitPos(self, x, y, w, h, margin = 0, bounce = False):
    if self.x<x+margin:
      self.x = x+margin
      if bounce:self._velocity.bounce_off(math.pi/2)
      else:self._velocity.addTo(self._velocity.clone().bounce_off(math.pi/2))
    if self.y<y+margin:
      self.y = y+margin
      if bounce:self._velocity.bounce_off(0)
      else:self._velocity.addTo(self._velocity.clone().bounce_off(0))
    if self.x>self.parent.size[0]-margin:
      self.x = self.parent.size[0]-margin
      if bounce:self._velocity.bounce_off(math.pi/2)
      else:self._velocity.addTo(self._velocity.clone().bounce_off(math.pi/2))
    if self.y>self.parent.size[1]-margin:
      self.y = self.parent.size[1]-margin
      if bounce:self._velocity.bounce_off(0)
      else:self._velocity.addTo(self._velocity.clone().bounce_off(0))
  
  def limitPosToScreen(self, bounce):
    self._limitPos(0,0,self.parent.size[0],self.parent.size[1],0,bounce)


class Vector(object):
  def __init__(self, t, m):
    self.degrees = t
    self.magnitude = m
    
  @classmethod
  def frompos(self, x, y):
    return Vector(math.atan2(y,x)*180/math.pi,math.sqrt(x*x+y*y))
  
  _get_x = lambda s:math.cos(s.theta)*s.magnitude
  _set_x = lambda s, x:setattr(s,'theta', math.atan2(s.y,x)) and setattr(s,'magnitude', math.sqrt(x**2+s.y**2))
  _get_y = lambda s:math.sin(s.theta)*s.magnitude
  _set_y = lambda s, x:setattr(s,'theta', math.atan2(y,s.x)) and setattr(s,'magnitude', math.sqrt(s.x**2+y**2))
  _get_degrees = lambda s:s.theta/math.pi*180
  _set_degrees = lambda s, x:setattr(s,'theta',x*math.pi/180)
  
  x = property(_get_x, _set_x)
  y = property(_get_y, _set_y)
  degrees = property(_get_degrees, _set_degrees)
  
  def __add__(self, other):
    return Vector.frompos(self.x + other.x, self.y + other.y)
    
  def bounce_off(self, angle):
  	self.theta = angle*2 - self.theta
  	return self
  
  def part(self, angle):
    return Vector(angle, math.cos(angle-self.theta)*self.magnitude)
  
  def clone(self):
    return Vector(self.theta,self.magnitude)
  
  def reverse(self):
    return Vector(self.degrees+180,self.magnitude)
  
  def set(self, v, relative):
    if (relative):
      v += self
    self.theta = v.theta
    self.magnitude = v.magnitude

class Group:
  def __init__(self):
    #self.plain = []
    self.dcts = {Object:[]}
  
  def add(self, obj):
    if obj in self.dcts[Object]:
      raise Exception,'object already in group'
    #self.plain.append(obj)
    for cls in inspect.getmro(obj.__class__):
      if not self.dcts.has_key(cls):
        self.dcts[cls] = []
      self.dcts[cls].append(obj)
      if cls == Object:
        return
  append = add
  
  def remove(self, obj):
    for cls in inspect.getmro(obj.__class__):
      if self.dcts.has_key(cls) and obj in self.dcts[cls]:
        self.dcts[cls].remove(obj)
      if cls == Object:
        return
  
  def get(self, cls):
    return self.dcts.get(cls,[])

class Game:
  def __init__(self, images, objectdict, maps, raw_images):
    self.images = images          # (name=>image obj)
    self.objectdict = objectdict  # (name=>class)
    self.maps = maps              # (name=>map obj)
    self.textures = {}
    self.fps = 40
    self.clock = pygame.time.Clock()
    self.raw_images = raw_images
  
  def preload_images(self, images):
    for im in images:
      self.textures[im] = fixrabbyt.load_and_size(im).id
  
  def send(self,name,*args,**kwds):
    ## optimize -- only go through those that have the event defined?
    [getattr(obj, name)(*args, **kwds) for obj in self.objects.get(Object)]
    
  def start(self, mapname):
    cmap = self.maps[mapname]
    if cmap.has_key('fps'):self.fps = cmap['fps']
    self.size = cmap['width'],cmap['height']
    pygame.display.set_mode((cmap['width'], cmap['height']), pygame.OPENGL | pygame.DOUBLEBUF)
    rabbyt.set_viewport((cmap['width'], cmap['height']), (0,0,cmap['width'], -cmap['height']))
    rabbyt.set_default_attribs()
    self.preload_images(self.raw_images)
    
    self.objects = Group()
    for item in cmap['items']:
      self.objects.append(self.objectdict[item['name']](self, item['x'], item['y']))
    self.loop()
  
  def events(self):
    for event in pygame.event.get():
      if event.type==QUIT:
        self.running = False
        return
      self.send('event', event)
  
  def step(self):
    self.send('_step')
  
  def draw(self):
    rabbyt.clear((255,255,255,1))
    rabbyt.render_unsorted(self.objects.get(Object))
  
  def loop(self):
    self.running = True
    while self.running:
      self.events()
      self.step()
      self.draw()
      pygame.display.flip()
      self.clock.tick(self.fps)

