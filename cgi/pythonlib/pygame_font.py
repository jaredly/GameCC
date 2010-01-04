from __future__ import division
import rabbyt
import pygame

default_alphabet = ("0123456789"
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    "abcdefghijklmnopqrstuvwxyz"
                    "{}()[]<>!?.,:;'\"*&%$@#\/|+=-_~`")

def next_power_of_2(v):
    v = int(v)- 1
    v |= v >> 1
    v |= v >> 2
    v |= v >> 4
    v |= v >> 8
    v |= v >> 16
    return v + 1

class Font(object):
    """
    ``Font(pygame_font, [alphabet])``

    Holds the information for drawing a font.

    ``pygame_font`` should be a ``pygame.font.Font`` instace.

    ``alphabet`` is a string containing all of the characters that should
    be loaded into video memory.  It defaults to
    ``rabbyt.fonts.default_alphabet`` which includes numbers, symbols, and
    letters used in the English language.

    To actually draw a font you need to use a ``FontSprite``.

    The characters will be rendered onto an OpenGL texture.
    """
    def __init__(self, pygame_font, alphabet=default_alphabet):
        self.pygame_font = pygame_font
        self.alphabet = alphabet
        widest = max(self.pygame_font.size(char)[0]+1 for char in alphabet)
        height = self.pygame_font.size(" ")[1]

        total_area = widest*height*len(self.alphabet)
        sw = sh = total_area**.5
        sw += widest
        sh += height
        sw = next_power_of_2(sw)
        sh = next_power_of_2(sh)

        surface = pygame.Surface((sw, sh), pygame.SRCALPHA, 32)

        self.coords = {}
        x=0
        y=0
        for char in alphabet:
            w = self.pygame_font.size(char)[0]
            self.coords[char] = (x/sw, 1-y/sh, (x+w)/sw, 1-(y+height)/sh)
            surface.blit(
                    self.pygame_font.render(char, True, (255,255,255)), (x,y))
            x += widest
            if x + widest > sw:
                y += height
                x = 0

        data = pygame.image.tostring(surface, "RGBA", True)
        self._texture_id = rabbyt.load_texture(data, (sw, sh))
        self.height = height
        self.space_width = pygame_font.size(" ")[0]

    def _get_texture_id(self):
        return self._texture_id
    texture_id = property(_get_texture_id, doc=
        """
        This is the id of the OpenGL texture for this font.  The texture will
        be unloaded when the font is garbage collected.
        """)

    def get_char_tex_shape(self, char):
        """
        ``get_char_tex_shape(char)``

        Returns the texture shape of the given character in the form of
        ``(left, top, right, bottom)``.

        ``KeyError`` is raised if ``char`` is not in the font's ``alphabet``.
        """
        return self.coords[char]

    def get_char_width(self, char):
        """
        ``get_char_width(char)``

        Returns the width in pixels of the given character.
        """
        return self.pygame_font.size(char)[0]

    def __del__(self):
        if rabbyt:
            rabbyt.unload_texture(self.texture_id)

class FontSprite(rabbyt.BaseSprite):
    """
    ``FontSprite(font, text, ...)``

    A sprite that displays text from a ``Font``.

    ``font`` should be a ``rabbyt.fonts.Font`` instance to be used.

    ``text`` is the string to be displayed!  (It can be changed later with
    the text property.)

    This inherits from ``BaseSprite``, so you can use all of the
    transformation and color properties.
    """
    def __init__(self, font, text, **kwargs):
        rabbyt.BaseSprite.__init__(self, **kwargs)
        self.font = font
        self.texture_id = font.texture_id
        self.text = text

    def _get_text(self):
        return self._text
    def _set_text(self, text):
        self._text = text
        h = self.font.height
        x = 0
        self.char_sprites = []
        for i, char in enumerate(text):
            if not char in self.font.alphabet:
                x += self.font.space_width
                continue
            w = self.font.get_char_width(char)
            l, t, r, b = self.font.get_char_tex_shape(char)
            self.char_sprites.append(rabbyt.Sprite(texture=self.texture_id,
                    shape=(x, 0, x+w, -h),
                    tex_shape=self.font.get_char_tex_shape(char),
                    rgba=self.attrgetter('rgba')))
            x += w+1
    text = property(_get_text, _set_text, doc="the text to be displayed")

    def render_after_transform(self):
        rabbyt.render_unsorted(self.char_sprites)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)
    rabbyt.set_viewport((640, 480))
    rabbyt.set_default_attribs()

    font = Font(pygame.font.Font(pygame.font.get_default_font(), 20))
    sprite = FontSprite(font, "hello world")
    sprite.rot = rabbyt.lerp(0, 360, dt=6, extend="repeat")
    sprite.x = 100
    sprite.rgb = 0,1,1

    while not pygame.event.get(pygame.QUIT):
        rabbyt.clear((0,.5,.5,1))
        rabbyt.set_time(pygame.time.get_ticks()/1000)
        sprite.render()
        pygame.display.flip()
