
var MapAsset = Class([Asset], {
  type: 'map',
  add_item: function(self, item) {
    // implement a "item changes queue", which will aggregate additions/removals
    // and post all changes 2 seconds after the last change -- or after...
    // ...20 changes are made? maybe.
    self.parent.ajax.send_queued('maps/add_item', {item:jsonify(item),'name':self.info.name}, null);
    self.info.items.push(item);
  },
  remove_item: function(self, item) {
    self.parent.ajax.send_queued('maps/remove_item', {item: jsonify(item), name:self.info.name}, null);
    self.info.items.splice(self.info.items.indexOf(item),1);
  },
  name_changed:function (self, type, from, to) {
    if (type == 'object') {
      var dirty = false;
      for (var i=0;i<self.info.items.length;i++){
        if (self.info.items[i]['name'] == from){
          self.info.items[i]['name'] = to;
          dirty = true;
        }
      }
      if (dirty){
        self.set_attr('items',self.info.items);
      }
    }
  }
});
