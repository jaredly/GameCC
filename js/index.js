
/**
    get plugins
        list_plugins -> handled by "PluginManager"
        async -- load each plugin. show loading bar
    list projects
        dialog box: open or new
        handled by "OpenDialog"
    to load a project:
        load_project -> {metadata, images, objects, maps, rawimages}
            handled by "Project" object


**/

/**
    Editor: main gamecc editor class
**/
var Editor = Class([], {
    /*good*/
    __init__: function(self){
        self._small = true;
        self.ajax = AjaxMuffin(self);
        self.errors = ErrorManager(self);
        self.imagescale = ImageScale(self);
        self.imagepicker = ImagePicker(self);
        self.media = MediaLibrary(self);
        self.tabs = TabMan(self, self.onTabChange, self.onRightClick);
        self.plugins = PluginManager(self);
        self.namedialog = NameDialog();
        self.project = Project(self, {
            'load':self._onload,
            'delete':self.clear,
            'loadAsset':self.loadAsset,
        });
        self.project_dialog = ProjectDialog(self, {
            'open':self.onopen,
            'new':self.onnew,
            'remove':self.onremove
        });
        self.loadbar = LoadingBar(self.project.doneloading);
        self.display = {};
        self.display['image']    = DisplayImage(self);
        self.display['object'] = DisplayObject(self);
        self.display['map']        = DisplayMap(self);
        if (document.location.hash.slice(1)){
            self.project.open(document.location.hash.slice(1));
        }else{
            self.project_dialog.open();
        }
    },
    /*good*/
    loadAsset: function(self, type, id){
        var name = self.project.data[type][id].info.name;
        self.tabs.add(type, id, name, !self.project.loading);
        /*if (!self.project.loading) {
            self.display[type].selectname();
        }*/
    },
    /*good*/
    onTabChange: function(self, from, to){
        if (from){
            self.display[from[0]].unload();
        }
        self.display[to[0]].load(to[1]);
    },
    /*good -- right click callback for asset sidebar*/
    onRightClick: function(self, event, type, id){
        contextMenu([['Delete',self.removeAsset(type, id)],
            ['Clone', self.cloneAsset(type, id)]])(event);
    },
    /*good*/
    removeAsset: function(self, type, id){
        return function(){
            if (self.display[type].object === self.project.data[type][id]){
                self.display[type].unload();
            }
            self.project.remove(type, id);
            self.tabs.remove(type, id);
        };
    },
    /*good*/
    cloneAsset: function(self, type, id){
        return function(){
            self.project.clone(type, id);
        };
    },
    /*good*/
    onopen: function(self, id){
        self.clear();
        self.project.open(id);
    },
    /*good*/
    onnew: function(self, id){
        self.clear();
        self.namedialog.open(self.project.new);
    },
    /* -- look into -- */
    onremove: function(self, id){
        self.project.remove(id);
    },
    /*good*/
    clear: function(self){
        self.tabs.clear('image');
        self.tabs.clear('object');
        self.tabs.clear('map');
        self.display['image'].unload();
        self.display['object'].unload();
        self.display['map'].unload();
    },
    /*good*/
    imgurl: function(self, name){
        if (!name){
            return 'images/noimg.png';
        }
        return 'raw_images/' + name;
    },
    objImage: function(self, id){
        var obj = self.project.data['object'][id];
        if (!obj.info.image || !self.project.data['image'][obj.info.image]
                || !self.imgurl(self.project.data['image'][obj.info.image].info.subimages.length)){
            return self.imgurl(null);
        }
        return self.imgurl(self.project.data['image'][obj.info.image].info.subimages[0]);
    },
    objScaled: function(self, id, size) {
        var iid = self.project.data['object'][id].info.image;
        if (!iid || !self.project.data['image'][iid]
                || !self.imgurl(self.project.data['image'][iid].info.subimages.length)){
            return self.imagescale.get_scaled(null, size);
        }
        return self.imagescale.get_scaled(self.project.data['image'][iid].info.subimages[0], size);
    },
    /** TODO change name... and add killpreview **/
    preview: function(self) {
        self.ajax.send('project/preview',{},function(res){
            openIframe('preview/'+res.name+'.html',function(){},res.width,res.height);
        });
    }
});


var gcc;
$(function(){
    gcc = Editor();
});
