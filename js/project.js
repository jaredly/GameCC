
/**
    Game Info???
    = Title
    = game variables
    = Author
    = Description
**/

var Project = Class([], {
    assetTypes: {'image':ImageAsset, 'object':ObjectAsset, 'map':MapAsset},
    __init__:function(self, parent, callbacks){
        var defaults = {
            'new':function(){},
            'clone':function(){},
            'delete':function(){},
            'open':function(){},
            'loadAsset':function(){}
        };
        self.callbacks = $(defaults).extend(callbacks);
        self.parent = parent;
        self.info = {};
        self.loading = false;
    },
    'new': function(self, name){
        name = name || '';
        self.parent.ajax.send('project/new',{name:name},self._load);
    },
    open: function(self, name){
        if (!name)return;
        document.location.hash = name;
        self.parent.ajax.send('project/load',{name:name},self._load);
    },
    clear: function(self){
        self.data = {'image':{},'object':{},'map':{}};
        self.info = {};
    },
    add: function(self, type){
        self.parent.ajax.send(type+'s/new',{},self._loadasset(type));
    },
    remove: function(self, type, id){
        self.parent.ajax.send(type+'s/delete',{id:id},function(){delete self.data[type][id];});
    },
    clone: function(self, type, id){
        self.parent.ajax.send(type+'s/clone',{id:id},self._loadasset(type));
    },
    _load: function(self, result){
        self.clear();
        self.info = result.project;
        self.pid = self.info.pid;
        self.loading = true;
        self.parent.loadbar.load(result.project.images.length);
        self.loadassets('image', result.images);
        self.loadassets('object', result.objects);
        self.loadassets('map', result.maps);
        if (!self.info.images.length){
            self.parent.loadbar.close();
        }else
            self.parent.media.load(self.info.images);
    },
    doneloading: function(self){
        self.loading = false;
    },
    save_order: function(self, type, ids) {
        self.parent.ajax.queue(type + '/save_order', {names:jsonify(ids)},function(){});
    },
    add_images: function(self, images, func){
        self.parent.ajax.queue('project/add_images',{images:jsonify(images)},func||function(){});
    },
    check_name:function(self, type, name){
        for (var id in self.data[type]){
            if (self.data[type][id].info.name == name)return true;
        }
        return false;
    },
    loadassets: function(self, type, objects){
        for (var i=0;i<objects.length;i++){
            self._loadasset(type)(objects[i]);
        }
    },
    _loadasset: function(self, type){
        return function(result){
            self.data[type][result.id] = self.assetTypes[type](self.parent, result);
            self.callbacks.loadAsset(type, result.id);
        };
    },
    change_asset: function(self, type, id, to){
        if (self.check_name(type,to))return false;
        if (to.replace(/[^\w_]/g,'') !== to){
            return false;
        }
        self.data[type][id].info.name = to;
        self.parent.tabs.change(type, id, to);
//        self.register_name_changed(type, id, to);
        return to;
    },
    preview_name: function(self, type, id, to) {
        self.parent.tabs.preview(type, id, to);
    },
/*    register_name_changed: function(self, type, from, to){
        for (var atype in self.data){
            for (var name in self.data[atype]){
                self.data[atype][name].name_changed(type, from, to);
            }
        }
    }*/
});
