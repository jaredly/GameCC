import pygame
from pygame.locals import *
import random as Random
import math

class Game:
  def __init__(self, images, objects, maps, startingmap):
    self.screen = pygame.display.set_mode((500,500))
    self.objects = []
    self.size = []
    self.keys = []
    self.map = []
    self.maps = maps
    self.objectdict = objects
    self.images = images
    self.log = 'No errors'
    self.running =  False
    self.load_map(startingmap);
    self.clock = pygame.time.Clock()
  
  def events(self):
    for e in pygame.event.get():
      if e.type==QUIT:
        self.running = False
      self.event(e)
  
  def event(self,event):
    callbacks = {MOUSEBUTTONDOWN:'mouse_down', MOUSEBUTTONUP:'mouse_up', MOUSEMOTION:'mouse_move',
            KEYDOWN:'_key_down', KEYUP:'_key_up'}
    if event.type in callbacks:
      [getattr(o,callbacks[event.type])(event) for o in self.objects]
  
  def load_map(self, mapname):
    self.map = self.maps[mapname]
    self.objects = []
    self.size = self.map['size']
    self.screen = pygame.display.set_mode(self.size)
    for i in self.map['items']:
      self.objects.append(self.objectdict[i['name']](self,Point(i['x'],i['y'])))
  
  def remove(self, object):
    self.objects.remove(object)
  
  def loop(self):
    self.running = True
    while self.running:
      self.events()
      self.step()
      self.draw()
      pygame.display.flip()
      self.clock.tick(40)
  
  def step(self):
    [o._step() for o in self.objects]
  
  def draw(self):
    self.screen.fill((255,255,255))
    [obj.draw(self.screen) for obj in self.objects]

class Vector:
  def __init__(self, t, m):
    self.t=t
    self.m=m
    
  @classmethod
  def frompos(self, x, y):
    return Vector(math.atan2(y,x),math.sqrt(x*x+y*y))
  
  def x(self):
    return math.cos(self.t)*self.m
  
  def setx(self, nx, relative):
    if (relative):
      nx += self.x()
    nv = Vector.frompos(nx,self.y())
    self.t=nv.t
    self.m=nv.m
  
  def y(self):
    return math.sin(self.t)*self.m
  
  def sety(self, ny, relative):
    if (relative):
      ny += self.y()
    nv = Vector.frompos(self.x(),ny)
    self.t=nv.t
    self.m=nv.m
  
  def add(self, v):
    return Vector.frompos(self.x() + v.x(), self.y()+v.y())
  
  def addTo(self, v):
    nv = self.add(v)
    self.t=nv.t
    self.m=nv.m
  
  def bounce_off(self, angle):
  	self.t = angle*2 - self.t
  	return self
  
  def part(self, angle):
    return Vector(angle, math.cos(angle-self.t)*self.m)
  
  def clone(self):
    return Vector(self.t,self.m)
  
  def reverse(self):
    return Vector(self.t+math.pi,self.m)
  
  def set(self, v, relative):
    if (relative):
      self.add(v)
    else:
      self.t = v.t
      self.m = v.m

class Point:
  def __init__(self,x,y):
    self.x=x
    self.y=y
  def pos(self):
    return self.x,self.y

class Color:
  @classmethod
  def rgb( r, g, b ):
    return (r << 16) | (g << 8) | b

