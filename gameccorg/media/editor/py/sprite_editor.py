
from asset_editor import AssetEditor, ajax

jq = window.jQuery
ext = window.Ext

def jq_list(sel):
    elms = js.jq(sel)
    return [js.elms[i] for i in range(elms.length)]

class SpriteEditor(AssetEditor):
    asset_type = 'sprite'
    def __init__(self, parent):
        AssetEditor.__init__(self, parent)
        js.jq('#sprite-subimages').sortable({'stop':self.sorted, 'placeholder':'sort-helper'}).droppable({'drop':self.dropImage})

    def load(self, aid):
        AssetEditor.load(self, aid)
        self.load_subimages()

    def load_subimages(self):
        js.jq('#sprite-subimages .item').remove()
        for pk in self.current['fields']['subimages']:
            self.addImage(pk)
        if not len(self.current['fields']['subimages']):
            js.jq('#sprite-info .sprite-top').css('background-image', 'url(/media/editor/images/add-image.png)')

    def addImage(self, pk):
        div = self.parent.media.image_div(pk, 'medium')
        js.jq('#sprite-subimages').append(div)
        self.do_subimages()

    def do_subimages(self):
        print 'yep'
        self.set_attr('subimages', self.get_subimages())
        first = self.current['fields']['subimages'][0]
        js.jq('#sprite-info .sprite-top').css('background-image', 'url(' + self.parent.media.image_src(first, 'large') + ')')
        ajax.send('sprite/' + str(self.current['pk']) + '/save_subimages', {'subimages': self.current['fields']['subimages']})
        print 'just sent'

    def get_subimages(self):
        return [int(str(node.id).split('-')[-1]) for node in jq_list('#sprite-subimages .item') if node.id]

    def dropImage(self, event, ui):
        print 'dropped'
        source = js.ui.draggable.parent()[0].id
        if source == 'media-images':
            theid = str(js.ui['draggable'][0].id)
            pk = int(theid.split('-')[-1])
            self.current['fields']['subimages'].append(pk)
            self.addImage(pk)
            print 'howdy'
    
    def sorted(self, event, ui):
        print 'sorted it all'
        self.do_subimages()

# vim: et sw=4 sts=4
