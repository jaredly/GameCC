
var ImageAsset = Class([Asset], {
    type: 'image',
    set_images:function(self, subimages, callb){
        self.info.subimages = subimages;
        self.parent.ajax.queue('images/set_attr', {id:self.info['id'], attr:'subimages', value:jsonify(subimages)},
            function(){
                callb();
            });
        /*self.parent.ajax.send_queued('images/set_attr',{name:self.info.name, attr:'subimages', value:jsonify(subimages)},function(){
            self.info.subimages = subimages;
            callb();
        });*/
    },
    add_image:function(self, name, callb){
        self.info.subimages.push(name);
        self.set_images(self.info.subimages, callb);
    },
    name_changed:function(self){}
});
