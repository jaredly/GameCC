#!/usr/bin/env python

class Game:
    objects = {}
    maps = {}
    sprites = {}
    info = {'fullscreen':False}

    def __init__(self):
        self.window = pyglet.window.Window(fullscreen=self.info['fullscreen'],
                vsync=True)
        self.map = maps[0](self)
        self.window.set_size(self.map.size)
        ## ok so the map will handle the Objects, and the Camera, and... anyway.
        ## event handlers.
        for func in dir(self):
            if func.startswith('on_'):
                setattr(self.window, func, getattr(self, func))

    def send(self, name, args):
        for obj in self.map.objs:
            getattr(obj, name)(*args)

    def on_mouse_drag(self, x, y, dx, dy, buttons, mods):
        self.send('on_mouse_drag' % button, (x, y, dx, dy))
        for button in buttons:
            self.send('on_mouse_drag_%d' % button, (x, y, dx, dy))

    def on_mouse_motion(self, x, y, dx, dy):
        self.send('on_mouse_motion', (x, y, dx, dy))

    def on_mouse_press(self, x, y, button, mods):
        self.send('on_mouse_press', (x, y))
        self.send('on_mouse_press_%d' % button, (x, y))

    def on_mouse_release(self, x, y, button, mods):
        self.send('on_mouse_release', (x, y))
        self.send('on_mouse_release_%d' % button, (x, y))

    ###### game control methods ; accessible by objects ######

    def next_map(self):
        pass

    def prev_map(self):
        pass

    def reload_map(self):
        pass

    def load_map(self, map):
        pass

    def restart_game(self):
        pass

    def exit_game(self):
        pass



# vim: et sw=4 sts=4
