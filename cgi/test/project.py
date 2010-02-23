import os

import magic
from ..base import drupal
from ..base import projectman as project
from ..base import asset

DATADIR = os.path.join(os.path.dirname(__file__), 'data')

class Test(magic.MagicTest):

    def newProject(self):
        self.assertEqual(project.list_projects(), [])
        all = project.new('Proj')
        self.assert_(all)
        self.assertEqual(all['project']['pid'], 1)
        for n in ('images', 'maps', 'objects'):
            self.assertEqual(all[n],[])

    def addImages(self):
        self.assertRaises(project.ImageError, project.add_images,(['one.png'],))
        project.uploadimage('one.png',open(os.path.join(DATADIR, 'one.png')).read())
        self.assertEqual(project.list_images(),[u'one.png'])

    def listProjects(self):
        self.assertEqual(project.list_projects(), [u'Proj'])

