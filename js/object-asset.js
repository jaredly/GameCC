/** encode action datatype */
var ObjectAsset = Class([Asset], {
    type: 'object',
    name_changed: function(self, type, from, to){
        /*if (type == 'image' && self.info.image == from){
            self.set_attr('image', to);
        }
        if (type == 'object') {
            if (self.info.parent === from) {
                self.set_attr('parent',to);
            }
            for (var event in self.info.events) {
                if (event.indexOf('collide_') === 0 && event.slice('collide_'.length) == from) {
                    self.change_event(event, 'collide_' + to);
                    event = 'collide_' + to;
                }
                var dirty = false;
                for (var i=0;i<self.info.events[event].length;i++) {
                    for (var attr in self.info.events[event][i][1]) {
                        if (self.info.events[event][i][1][attr][0] == 'object'){
                            if (self.info.events[event][i][1][attr][1] == from){
                                self.info.events[event][i][1][attr][1] = to;
                                dirty = true;
                            }
                        }
                    }
                }
                if (dirty) {
                    self.save_actions(event, self.info.events[event]);
                }
            }
        }*/
    },
    add_event: function(self, type) {
        if (self.info.events[type]){
            return false;
        }
        self.parent.ajax.queue('objects/add_event',{'id':self.info.id, 'event':type});
//        self.parent.ajax.send_queued('objects/add_event',{'name':self.info.name,'event':type});
        self.info.events[type] = [];
        return true;
    },
    remove_event:function(self,type){
        if (!self.info.events[type]){
            return false;
        }
        self.parent.ajax.queue('objects/remove_event', {'id':self.info.id, 'event':type});
//        self.parent.ajax.send_queued('objects/remove_event',{'name':self.info.name,'event':type});
        delete self.info.events[type];
        return true;
    },
    change_event:function(self, event, name, func){
        self.parent.ajax.queue('objects/change_event',{'id':self.info.id,'event':event,'nevent':name},function(res){
            func && func();
        });
        self.info.events[name] = self.info.events[event];
        delete self.info.events[event];
    },
    duplicate_event:function(self, orig, dup, func){
        self.parent.ajax.queue('objects/duplicate_event',{'id':self.info.id,'event':orig,'nevent':dup},function(res){
            self.info.events[dup] = res.actions;
            func();
        });
    },
    save_actions: function(self, event, actions) {
        self.info.events[event] = actions;
        var json = jsonify(self.info.events[event]);
        self.parent.ajax.queue('objects/save_actions',{'id':self.info.id,'event':event,'actions':json});
    }
});
