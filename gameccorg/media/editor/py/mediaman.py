#!/usr/bin/env python

import json
from sizecache import SizeCache

from ajax import ajax

jq = window.jQuery

class MediaManager:
    def __init__(self, parent):
        self.parent = parent
        window.layouts['new-image']['buttons'][0]['handler'] = self.onOk
        window.layouts['new-image']['buttons'][1]['handler'] = self.onCancel
        self.dlg = new(window.Ext.Window(window.layouts['new-image']))
        js.jq('#media-images .item.new').click(self.newImage)
        self.cache = SizeCache()

    def newImage(self, event):
        self.dlg.show()

    def reloadFrame(self):
        parent = js.jq('#new-image-dlg iframe').parent()
        js.jq('#new-image-dlg iframe').remove()
        js.parent.append('<iframe src="/editor/upload/image/"></iframe>');

    def onOk(self, *a, **b):
        doc = js.jq('#new-image-dlg iframe').load(self.doneLoading).contents()[0].documentElement
        js.jq('form', doc).submit()

    def onCancel(self, *a, **b):
        self.dlg.hide()

    def doneLoading(self, event):
        iframe = js.jq('#new-image-dlg iframe')
        doc = js.iframe.contents()
        doc = js.doc[0].documentElement
        new_model = py(json.loads(js.jq('body', doc).html()))[0]
        pk = new_model['pk']
        self.images[pk] = new_model
        self.cache_image(pk)
        self.reloadFrame()
        self.dlg.hide()

    def load(self, media_url, models, loader):
        self.media_url = media_url
        loader.setMessage('Loading Media')
        loader.total += len(models) - 1
        def imgLoaded(event=None):
            loader.increment()
            if loader.isDone():
                loader.done()
        self.images = {}
        for model in models:
            pk = model['pk']
            if model['model'] == 'gcc_media.image':
                self.images[pk] = model
                self.cache_image(pk, imgLoaded)

    def cache_image(self, pk, cb=None):
        model = self.images[pk]
        def done_caching():
            if cb:
                cb()
            self.addImage(model)
        self.cache.cache(self.media_url + model['fields']['image'], done_caching)

    def addImage(self, model):
        src = self.media_url + model['fields']['image']
        data = self.cache.caches['medium'][src]
        img = self.cache.caches['full'][src]
        div = js.jq('''<div class="item">
                    <div class="img">
                        <div class="hover">''' + str(img.width) + 'x' + str(img.height) + '<br/>' + model['fields']['image'].split('/')[-1] + '''
                        <div class="delete"></div>
                        </div>
                    </div>
                </div>''').appendTo(js('#media-images'))
        js.jq('>div', div).css(js('background-image'), js('url(' + data + ')'))
        def remove(event):
            self.removeImage(model)
            js.div.remove()
        js.jq('.delete', div).click(remove)

    def removeImage(self, model):
        ajax.send('media/remove', {'type':'image', 'pk':model['pk']})

# vim: et sw=4 sts=4
