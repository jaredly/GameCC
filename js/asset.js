var Asset = Class([], {
    type: null,
    __init__: function (self, parent, info) {
        self.parent = parent;
        self.info = info;
    },
    set_name:function(self,newname){
        if (self.type == 'object'){
            newname = totitle(newname);
        }
        if (newname.replace(/[^\w_]/g,'')!==newname){
            self.preview_name(self.info.name);
            return self.info.name;
        }
        if (self.parent.project.check_name(self.type,newname)){
            self.preview_name(self.info.name);
            return self.info.name;
        }
        var old = self.info.name;
        var name = self.parent.project.change_asset(self.type, self.info.id, newname);
        if (name){
            self.parent.ajax.queue(self.type+'s/rename', {'id':self.info.id, 'new':name});
        } else {
            self.preview_name(self.info.name);
        }
        return name;
    },
    preview_name:function(self, name) {
        self.parent.project.preview_name(self.type, self.info.id, name);
    },
    set_attr:function(self,attr,value, ondone){
        ondone = ondone || function(){};
        self.parent.ajax.queue(self.type+'s/set_attr', {'id':self.info.id, 'attr':attr, 'value':jsonify(value)}, function(){ondone && ondone(value);});
        self.info[attr]=value;
    },
    reload:function(self){
        self.parent.ajax.queue(self.type+'s/load', {'id':self.info.id}, function(result) {
            self.__init__(self.parent, result);
        });
    },
});
