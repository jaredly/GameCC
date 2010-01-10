
var MapAsset = Class([Asset], {
    type: 'map',
    add_item: function(self, item) {
        // implement a "item changes queue", which will aggregate additions/removals
        // and post all changes 2 seconds after the last change -- or after...
        // ...20 changes are made? maybe.
        self.parent.ajax.send('maps/add_item', {item:jsonify(item),'id':self.info.id}, null);
        //self.parent.ajax.send_queued('maps/add_item', {item:jsonify(item),'name':self.info.name}, null);
        self.info.objects.push(item);
    },
    remove_item: function(self, item) {
        self.parent.ajax.queue('maps/remove_item', {item: jsonify(item), id:self.info.id}, null);
        //self.parent.ajax.send_queued('maps/remove_item', {item: jsonify(item), name:self.info.name}, null);
        self.info.objects.splice(self.info.objects.indexOf(item),1);
    },
    name_changed:function (self, type, from, to) {
        if (type == 'object') {
            var dirty = false;
            for (var i=0;i<self.info.objects.length;i++){
                if (self.info.objects[i]['name'] == from){
                    self.info.objects[i]['name'] = to;
                    dirty = true;
                }
            }
            if (dirty){
                self.set_attr('items',self.info.objects);
            }
        }
    }
});
