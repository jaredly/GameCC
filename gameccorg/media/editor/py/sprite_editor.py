
from asset_editor import AssetEditor, ajax

class SpriteEditor(AssetEditor):
    asset_type = 'sprite'
    def __init__(self, parent):
        AssetEditor.__init__(self, parent)

# vim: et sw=4 sts=4
