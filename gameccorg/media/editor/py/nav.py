
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

class NavMan:
    def __init__(self,  editor):
        self.editor = editor
        self.general_list = ClickableList(js.jq('#general-nav ul'))
        self.general_list.addListener(self.generalClick)

        #js.jq('#general-nav .project-info').click(self.show_project_info)
        #js.jq('#general-nav .media-manager').click(self.show_media_manager)

    def generalClick(self, what):
        if what == 'Project Info':
            js.ext.getCmp('main-content').layout.setActiveItem(0)
        elif what == 'Media Manager':
            js.ext.getCmp('main-content').layout.setActiveItem(1)
        

# vim: et sw=4 sts=4
