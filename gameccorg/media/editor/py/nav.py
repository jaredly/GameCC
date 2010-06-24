
from CSS import nav

jq = window.jQuery
ext = window.Ext

class ClickableList:
    def __init__(self, node=None):
        self.node = node
        js.node.click(self.onClick)
        self.listeners = []

    def addListener(self, what):
        self.listeners.append(what)

    def onClick(self, event):
        js.jq('.selected', self.node).removeClass(js('selected'))
        js.jq(event.target).addClass(js('selected'))
        for l in self.listeners:
            l(str(event.target.innerHTML))

    def clear_sel(self):
        js.jq('.selected', self.node).removeClass(js('selected'))

class NavMan:
    def __init__(self,  parent):
        self.parent = parent
        self.general_list = ClickableList(js.jq('#general-nav ul'))
        self.general_list.addListener(self.generalClick)
        self.setup_assets()

    def generalClick(self, what):
        if what == 'Project Info':
            js.ext.getCmp('main-content').layout.setActiveItem(0)
        elif what == 'Media Manager':
            js.ext.getCmp('main-content').layout.setActiveItem(1)
        else:
            return
        self.clearOthers(None)

    def reload(self, atype, cb=None):
        tree = window.Ext.getCmp(atype + '-tree')
        tree.loader.dataUrl = js('/editor/ajax/project/' + str(self.parent.pid) + '/folder/' + atype + '/')
        tree.getRootNode().reload(cb)

    def clearOthers(self, atype):
        alls = ['sprites', 'objects', 'maps']
        if atype is not None:
            alls.remove(atype)
            self.general_list.clear_sel()
        for at in alls:
            window.Ext.getCmp(at + '-tree').getSelectionModel().clearSelections()

    def setup_assets(self):
        window.Ext.getCmp('sprites-tree').getSelectionModel().on('selectionchange', self.onAsset)
        window.Ext.getCmp('objects-tree').getSelectionModel().on('selectionchange', self.onAsset)
        window.Ext.getCmp('maps-tree').getSelectionModel().on('selectionchange', self.onAsset)

    def onAsset(self, tree, node, event=None):
        if not node:return
        atype = str(tree.tree.id).split('-')[0]
        self.clearOthers(atype)
        self.parent.editors[atype].load(node.id)

# vim: et sw=4 sts=4
