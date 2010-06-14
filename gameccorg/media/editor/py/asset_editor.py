
from ajax import ajax

jq = window.jQuery

class AssetEditor:
    asset_type = None
    def __init__(self, parent):
        self.parent = parent
        window.Ext.getCmp('new-' + self.asset_type + '-button').on('click', self.new_)
        self.node = js.jq('#' + self.asset_type + '-editor')
        self.current = None

    def new_(self, button, event):
        ajax.send(self.asset_type + '/new', {'pid':self.parent.pid}, self.onNew)

    def onNew(self, data):
        self.parent.assets[self.asset_type + 's'][data['_models'][0]['pk']] = data['_models'][0]
        self.parent.nav.reload(self.asset_type+'s')

    def load(self, aid):
        window.Ext.getCmp('main-content').layout.setActiveItem(self.asset_type + '-editor')
        self.current = self.parent.assets[self.asset_type + 's'][aid]
        js.jq('.title', self.node).val(self.current['fields']['title'])




# vim: et sw=4 sts=4
