import magic

from ..base import drupal
from ..base import images

class Test(magic.MagicTest):

    def newImage(self):
        self.assertEqual(images.list(),[])
        all = images.new()
        self.assertEqual(all['name'], 'Image')
        im2 = images.new()
        self.assertEqual(im2['name'], 'Image 2')
        self.assertEqual(im2['id'], 2)
        self.imd = im2['id']

    def cloneImage(self):
        cl = images.clone(self.imd)
        self.assertEqual(cl['name'], 'Image 2 Copy')

    def renameImage(self):
        images.rename(self.imd, 'Ralph')
        self.assertEqual(images.load(self.imd)['name'], 'Ralph')
    
    def deleteImage(self):
        images.delete(self.imd)
        self.assertThrows(asset.AssetException,
                images.load, self.imd)

