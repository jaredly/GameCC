from __future__ import division
import pygame, rabbyt, sys, os
import rabbyt
from rabbyt._rabbyt import load_texture


def next_pow2( n ):
    """
    Find the next power of two.
    """
    n -= 1
    n = n | (n >> 1)
    n = n | (n >> 2)
    n = n | (n >> 4)
    n = n | (n >> 8)
    n = n | (n >> 16)    
    n += 1
    return n

class Tex:
    def __init__(self):
        self.id = 0
        self.width = 0
        self.height = 0
        self.tex_coords = (0,0,0,0)

data_directory = 'data'

_texture_cache = {}
def load_and_size(filename, filter=True, mipmap=True):
    if filename not in _texture_cache:
        pygame = __import__("pygame", {},{},[])
        if os.path.exists(filename):
            img = pygame.image.load(filename)
        else:
            img = pygame.image.load(os.path.join(data_directory, filename))
        
        t = Tex()
        t.width,t.height = size = list(img.get_size())
        size[0] = next_pow2(size[0])
        size[1] = next_pow2(size[1])
        t.tex_coords = (0,t.height/size[1],t.width/size[0],0)
            
        n = pygame.Surface(size, pygame.HWSURFACE|pygame.SRCALPHA)
        #n.lock()
        #for x in range(size[0]):
        #  for y in range(size[1]):
        #    n.set_at((x,y),(0,100,0,10))
        #n.unlock()
        #n.fill((255,255,25,10))
        n.blit(img, (0,size[1]-t.height))
        
        data = pygame.image.tostring(n, 'RGBA', True)
        t.id = load_texture(data, size, 'RGBA', filter, mipmap)
        _texture_cache[filename] = t
    return _texture_cache[filename]

rabbyt.set_load_texture_file_hook(load_and_size)

