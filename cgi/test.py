from game import Game, ImageSprite, Point
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
  
  
  def keepOnScreen(bounce):
    self.limitPos(0,0,self.parent.size[0],self.parent.size[1],0,bounce)
  def setV(self,v,rel):
    if rel:
      self.v.addTo(v)
    else:
      self.v = v
  def createObject(self, object, x, y, relative, velocity):
    if relative:
      x+=self.pos.x
      y+=self.pos.y
    obj = self.parent.objectdict[object](self.parent,Point(x,y))
    obj.setV(velocity)
    self.parent.objects.append(obj)
  def moveToCollision(v, object):
    v.m/=10
    if self.collidesWith(object):
      for i in range(10):
        self.moveTo(-v.x(),-v.y(),true)
        if not self.collidesWith(object):
          return
    else:
      for i in range(10):
        this.moveTo(v.x(),v.y(),true)
        if self.collidesWith(object):
          self.moveTo(-v.x(),-v.y(),true)
          return
  def collisionAt(x, y, object):
    self.pos.x+=pos.x
    self.pos.y+=pos.y
    for obj in self.parent.objects:
      if obj==self:continue
      if obj.collidesWith(self):
        self.pos.x-=pos.x;self.pos.y-=pos.y;
        return True
    self.pos.x-=pos.x;self.pos.y-=pos.y
    return False
  def moveTo(x, y, relative):
    if relative:
      self.pos.x+=x
      self.pos.y+=y
    else:
      self.pos.x=x
      self.pos.y=y
  
  
  
  
  



class Msqymnyvaf:
  def __init__(self):
    objects = {};
    objects["Guy"] = Guy
    objects["Bullet"] = Bullet
    objects["Block"] = Block
    maps = {};
    maps["Mainard"] = {"persistant": false, "items": [{"y": 13, "x": 14, "name": "Block"}, {"y": 34, "x": 71, "name": "Block"}, {"y": 77, "x": 210, "name": "Block"}, {"y": 476, "x": 69, "name": "Block"}, {"y": 475, "x": 108, "name": "Block"}, {"y": 474, "x": 140, "name": "Block"}, {"y": 473, "x": 173, "name": "Block"}, {"y": 475, "x": 215, "name": "Block"}, {"y": 474, "x": 249, "name": "Block"}, {"y": 474, "x": 288, "name": "Block"}, {"y": 474, "x": 326, "name": "Block"}, {"y": 475, "x": 352, "name": "Block"}, {"y": 473, "x": 393, "name": "Block"}, {"y": 472, "x": 435, "name": "Block"}, {"y": 475, "x": 476, "name": "Block"}, {"y": 383, "x": 57, "name": "Block"}, {"y": 385, "x": 89, "name": "Block"}, {"y": 382, "x": 129, "name": "Block"}, {"y": 304, "x": 90, "name": "Block"}, {"y": 305, "x": 125, "name": "Block"}, {"y": 203, "x": 278, "name": "Block"}, {"y": 205, "x": 311, "name": "Block"}, {"y": 207, "x": 343, "name": "Block"}, {"y": 62, "x": 406, "name": "Block"}, {"y": 61, "x": 444, "name": "Block"}, {"y": 473, "x": 36, "name": "Block"}, {"y": 475, "x": 3, "name": "Block"}, {"y": 167, "x": 106, "name": "Guy"}, {"y": 9, "x": 419, "name": "Guy"}], "name": "Mainard", "size": [500, 500]}
    images = {};
    images["Block"] = {"src": "block.png", "name": "Block", "transparent": true}
    images["Guyi"] = {"src": "guy.png", "name": "Guyi", "transparent": true}
    images["bullet"] = {"src": "handle.png", "name": "bullet", "transparent": true}
    game = Game(images,objects,maps,"Mainard")



class Guy(ImageSprite):
  # any class variables (when I decide to include that) will go here
  def __init__(parent, pos, image="Guyi"):
    ImageSprite.__init__(self, parent, pos, image)
    
  
  def key_down_right_arrow():
    if (self.collisionAt(Point(0.0, 5.0), Block)){
    else:
    self.moveTo(5.0, 0.0, True);
    
    #super();
  
  def step():
    self.keepOnScreen(False);
    self.v.sety(0.1,True)
    #super();
  
  def key_down_left_arrow():
    pass
    #super();
  
  def key_down_up_arrow():
    pass
    #super();
  


class Bullet(ImageSprite):
  # any class variables (when I decide to include that) will go here
  def __init__(parent, pos, image="bullet"):
    ImageSprite.__init__(self, parent, pos, image)
    
  


class Block(ImageSprite):
  # any class variables (when I decide to include that) will go here
  def __init__(parent, pos, image="Block"):
    ImageSprite.__init__(self, parent, pos, image)
    
  


if __name__=='__main__':
  Msqymnyvaf()
