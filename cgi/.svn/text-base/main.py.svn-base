from game import Game, ImageSprite, Point, Vector
import pygame
from pygame.locals import *
'''
import game.Game;
import flash.geom.Point;
import flash.events.Event;
import flash.display.BitmapData;
import flash.display.Loader;
import flash.net.URLRequest;
import flash.ui.Keyboard;
'''


class BaseSprite(ImageSprite):
  
  
  
  
  def setV(self,v,rel):
    if rel:
      self.v.addTo(v)
    else:
      self.v = v
  def keepOnScreen(self,bounce):
    self.limitPos(0,0,self.parent.size[0],self.parent.size[1],0,bounce)
  def createObject(self, object, x, y, relative, velocity):
    if relative:
      x+=self.pos.x
      y+=self.pos.y
    obj = self.parent.objectdict[object](self.parent,Point(x,y))
    obj.setV(velocity)
    self.parent.objects.append(obj)
  def collisionAt(self, pos, object):
    self.pos.x+=pos.x
    self.pos.y+=pos.y
    for obj in self.parent.objects:
      if obj==self or not isinstance(obj, object):continue
      if obj.collidesWith(self):
        self.pos.x-=pos.x;self.pos.y-=pos.y;
        return True
    self.pos.x-=pos.x;self.pos.y-=pos.y
    return False
  def moveTo(self, x, y, relative):
    if relative:
      self.pos.x+=x
      self.pos.y+=y
    else:
      self.pos.x=x
      self.pos.y=y
  def moveToCollision(self, v, object):
    v.m/=10
    if self.collisionAt(Point(0,0), object):
      for i in range(10):
        self.moveTo(-v.x(),-v.y(),True)
        if not self.collisionAt(Point(0,0), object):
          return
    else:
      for i in range(10):
        self.moveTo(v.x(),v.y(),True)
        if self.collisionAt(Point(0,0), object):
          self.moveTo(-v.x(),-v.y(),True)
          return
  
  
  
  
  



class Xtwdecvugm:
  def __init__(self):
    objects = {};
    objects["Objects1"] = Objects1
    maps = {};
    maps["Maps1"] = {"persistant": False, "items": [{"y": 140, "x": 197, "name": "Objects1"}], "name": "Maps1", "size": [500, 500]}
    images = {};
    images["Images1"] = {"src": "object.png", "name": "Images1", "transparent": True}
    game = Game(images,objects,maps,"Maps1")
    game.loop()



class Objects1(BaseSprite):
  # any class variables (when I decide to include that) will go here
  def __init__(self, parent, pos, image="Images1"):
    BaseSprite.__init__(self, parent, pos, image)
    
  
  def step(self, ):
    pass
    #super();
  
  def create(self, ):
    self.setV(Vector(-0.739277047383, 3.4),True)
    #super();
  


if __name__=='__main__':
  Xtwdecvugm()
