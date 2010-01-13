import sys
sys.path.append('./temp/game/')
sys.path.append('./game/')
#import pygame
#from pygame.locals import *
import os

import random
Random = random

from game_pyglet import *

%(plugins_more)s

class %(name)s:
  def __init__(self):
    objects = {};
%(objects)s
    maps = {};
%(maps)s
    images = {};
%(images)s
    game = Game(images, objects, maps, %(images_more)s, BaseObject)
    game.start("%(maps_more)s")


%(objects_more)s

if __name__=='__main__':
  %(name)s()
