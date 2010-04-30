#!/usr/bin/env python

from gamecclib import Game

from objects import *
from maps import *

%(extra_imports)s

class %(project_name)s(Game):
    objects = {}
    maps = {} ## keys are both number 0 - num_maps and map names.
    sprites = {}
    info = {}

if __name__ == '__main__':
    %(project_name)s().run()
