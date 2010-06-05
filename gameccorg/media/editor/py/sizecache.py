#!/usr/bin/env python

jq = window.jQuery

class SizeCache:
    sizes = {
        'tiny': 16,
        'small': 32,
        'medium': 100,
        'large': 150,
    }
    def __init__(self):
        self.caches = {'full':{}}
        for k in self.sizes:
            self.caches[k] = {}

    def cache(self, src, ondone):
        if self.caches['full'].has_key(src):
            if ondone:
                ondone()
            return True

        def cached_full(event):
            for k in self.sizes:
                self.cache_one(src, k)
            if ondone:
                ondone()

        img = new(window.Image())
        img.src = src
        img.onload = js(cached_full)
        self.caches['full'][src] = img

        return False

    def cache_one(self, src, size):
        width = float(self.sizes[size])
        canvas = js.jq('<canvas class="caching" height="' + str(width) + '" width="' + str(width) + '"></canvas>')[0]
        ctx = canvas.getContext(js('2d'))
        img = self.caches['full'][src]
        if img.width > img.height:
            w,h = width, int(img.height*width/img.width)
            x,y = 0, width/2-h/2
        else:
            w,h = int(img.width*width/img.height), width
            x,y = width/2-w/2, 0
        ctx.drawImage(img, x, y, w, h)
        self.caches[size][src] = canvas.toDataURL()
        js.jq(canvas).remove()

# vim: et sw=4 sts=4
