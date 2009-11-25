
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
    self.parent.ajax.send('project/new',{project:name},self._load);
  },
  open: function(self, name){
    if (!name)return;
    self.parent.ajax.send('project/load',{project:name},self._load);
  },
  clear: function(self){
    self.data = {'image':{},'object':{},'map':{}};
    self.info = {};
  },
  add: function(self, type){
    self.parent.ajax.send(type+'s/new',{},self._loadasset(type));
  },
  remove: function(self, type, name){
    self.parent.ajax.send(type+'s/remove',{name:name},function(){delete self.data[type][name];});
  },
  clone: function(self, type, name){
    self.parent.ajax.send(type+'s/clone',{name:name},self._loadasset(type));
  },
  _load: function(self, result){
    self.clear();
    self.info = result.project;
    self.loading = true;
    self.parent.ajax.setloadbar(result.project.images.length, self.doneloading);
    self.parent.ajax.showStop();
    self.loadassets('image', result.images);
    self.loadassets('object', result.objects);
    self.loadassets('map', result.maps);
    if (!self.info.images.length){
      self.parent.ajax.unStop();
    }
    self.parent.media.load(result.project.images);
  },
  doneloading: function(self){
    self.loading = false;
  },
  save_order: function(self, type, names) {
    self.parent.ajax.send_queued(type + '/save_order', {names:jsonify(names)},function(){});
  },
  add_images: function(self, images, func){
    self.parent.ajax.send_queued('project/add_images',{images:jsonify(images)},func||function(){});
  },
  loadassets: function(self, type, objects){
    for (var i=0;i<objects.length;i++){
      self._loadasset(type)(objects[i]);
    }
  },
  _loadasset: function(self, type){
    return function(result){
      self.data[type][result.name] = self.assetTypes[type](self.parent, result);
      self.callbacks.loadAsset(type, result.name);
    };
  },
  change_asset: function(self, type, from, to){
    if (self.data[type][to])return false;
    if (to.replace(/[^\w_]/g,'') !== to){
      return false;
    }
    self.data[type][to] = self.data[type][from];
    self.data[type][to].info.name = to;
    self.parent.tabs.change(type, from, to);
    delete self.data[type][from];
    self.register_name_changed(type, from, to);
    return to;
  },
  preview_name: function(self, type, from, to) {
    self.parent.tabs.preview(type, from, to);
  },
  register_name_changed: function(self, type, from, to){
    for (var atype in self.data){
      for (var name in self.data[atype]){
        self.data[atype][name].name_changed(type, from, to);
      }
    }
  }
});
