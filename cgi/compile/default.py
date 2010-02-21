
class Asset:
    def __init__(self, parent, name, info):
        self.parent = parent
        self.name = name
        self.info = info

    def inline_output(self):
        return json.dumps(self.info)

    def output(self):
        return ''


class Compiler:
    otype = None
    asset_types = {'image':ImageAsset, 'object':ObjectAsset, 'map':MapAsset}
    basetemplate = ''
    maintemplate = ''
    ext = ''
    def __init__(self, db, pid, oname):
        self.db = db
        self.pid = pid
        self.oname = oname
        self.load_plugins()
        self.load_assets()

    def load_plugins(self):
        self.plugins = {}
        pnames = glob.glob(os.path.join(PLUGIN_DIR,
            "*/*.info"))
        for filename in pnames:
            name = filename.split('/')[-1].split('.')[0]
            self.plugins[name] = Plugin(self, name, filename)

    def load_assets(self):
        self.assets = {}
        for atype, AssetClass in self.asset_types.items():
            self.assets[atype] = {}
            items = self.db.find_dict(atype+'s',
                    {'pid': drupal.pid})
            for item in items:
                self.assets[atype][item['name']] =\
                        AssetClass(self, item)
    
    def output_base(self):
        data = {}
        
        return self.basetemplate % data

    def output_main(self):
        data = {}

        return self.maintemplate % data

    def compile(self, outname):
        tdir = tempfile.mkdtemp()
        odir = os.path.join(tdir, outname))
        basefile = os.path.join(odir, "BaseObject."+self.ext)
        mainfile = os.path.join(odir, "Main."+self.ext)
        imagedir = os.path.join(odir, 'images')

        os.mkdir(odir)
        os.mkdir(imagedir)
        base = self.output_base()
        open(basefile, 'w').write(base)
        main = self.output_main()
        open(mainfile, 'w').write(main)

        for image in self.list_images
        


