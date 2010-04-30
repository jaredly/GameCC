#!/usr/bin/env python
import pyglet
from pyglet import window, clock, font, image
from pyglet.gl import *

from world import World
from camera import Camera

class App(object):
    fullscreen = False
    fps = 40
    def __init__(self):
        self.window = pyglet.window.Window(fullscreen=self.fullscreen, vsync=True)
        self.map = 
        self.camera = Camera(self.win, scale = 1.0)
        clock.set_fps_limit(60)

    def mainLoop(self):
        while not self.win.has_exit:
            self.win.dispatch_events()

            self.step()
            self.world.step()

            self.camera.worldProjection()
            self.world.draw()

            self.camera.hudProjection()
            self.hud.draw()

            clock.tick()
            self.win.flip()


# vim: et sw=4 sts=4
