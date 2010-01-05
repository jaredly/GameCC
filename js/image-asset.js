
var ImageAsset = Class([Asset], {
    type: 'image',
    set_images:function(self, subimages, callb){
        self.parent.ajax.send_queued('images/set_attr',{name:self.info.name, attr:'subimages', value:jsonify(subimages)},function(){
            self.info.subimages = subimages;
            callb();
        });
    },
    add_image:function(self, name, callb){
        self.info.subimages.push(name);
        self.parent.ajax.send_queued('images/set_attr',{name:self.info.name, attr:'subimages', value:jsonify(self.info['subimages'])},function(){
            callb();
        });
    },
    name_changed:function(self){}
});
