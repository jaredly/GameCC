
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
    if (self.parent.project.data[self.type][newname]){
      self.preview_name(self.info.name);
      return self.info.name;
    }
    var old = self.info.name;
    var name = self.parent.project.change_asset(self.type, self.info.name, newname);
    if (name){
      self.parent.ajax.send_queued(self.type+'s/rename', {'name':old, 'new':newname});
    } else {
      self.preview_name(self.info.name);
    }
    return name;
  },
  preview_name:function(self, name) {
    self.parent.project.preview_name(self.type, self.info.name, name);
  },
  set_attr:function(self,attr,value, ondone){
    ondone = ondone || function(){};
    self.parent.ajax.send_queued(self.type+'s/set_attr', {'name':self.info.name, 'attr':attr, 'value':jsonify(value)}, function(){ondone && ondone(value);});
    self.info[attr]=value;
  },
  name_changed:function(self,type,from,to){
    console.error('name_changed not implemented for',self);
  },
  reload:function(self){
    self.parent.ajax.send_queued({'url':'projects/'+self.parent.project.info.name+'/'+self.type+'s/'+self.name,'func':function(result){
      self.__init__(self.parent,result);
    }});
  },
});
