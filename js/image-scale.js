
var ImageScale = Class([], {
    __init__: function(self, parent){
        self.parent = parent;
        self.cache = {};
        self.sizes = {'small':[25,25],'medium':[100,100],'large':[140,140]};
        self.scaled = {};
        self.back = new Image();
        self.back.src = 'images/alpha.png';
        self.defaultimg = new Image();
        self.defaultimg.src = 'images/no-image.png';
    },
    load: function(self, name, donefunc){
        if (self.cache[name])return donefunc(name);
        self.cache[name] = new Image();
        self.cache[name].onload = function(e){
            for (var size in self.sizes){
                self.scale(name, size);
            }
            self.parent.loadbar.increment();
            donefunc && donefunc(name);
        };
//        if (self.parent.ajax.stopped){
  //          self.parent.ajax.loading += 1;
    //    }
        self.cache[name].src = self.parent.imgurl(name);
    },
    scale: function(self, name, size){
        var width = self.sizes[size][0];
        var height = self.sizes[size][1];
        if (!self.scaled[name]){
            self.scaled[name] = {};
        }
        var canv = document.createElement('canvas');
        canv.style.visibility = 'hidden';
        canv.style.position='absolute';
        document.body.appendChild(canv);
        canv.width = width;
        canv.height = height;
        var ctx = canv.getContext('2d');
        for (var x=0;x<5;x++){
            for (var y=0;y<5;y++){
                ctx.drawImage(self.back, x*width/5, y*height/5, width/5, height/5);
            }
        }

        var oratio = self.cache[name].width/self.cache[name].height;
        var nratio = width/height;
        var nh,nw;
        if (nratio > oratio) {
            nh = height;
            nw = nh * oratio;
        } else {
            nw = width;
            nh = nw / oratio;
        }

        ctx.drawImage(self.cache[name], 0 + width/2-nw/2, 0 + height/2-nh/2, nw, nh);
        var nimg = new Image();
        nimg.src = canv.toDataURL();
        canv.parentNode.removeChild(canv);
        nimg.owidth = self.cache[name].width;
        nimg.oheight = self.cache[name].height;
        self.scaled[name][size] = nimg;
    },
    get_scaled: function(self, name, size){
        if (!name)return {src:''};
        if (!self.scaled[name])return {src:'raw_images/'+name};
        return self.scaled[name][size];
    },
    objCache: function(self, id) {
        var imgname = self.parent.project.data['image'][self.parent.project.data['object'][id].info.image].info.subimages[0];
        if (!self.cache[imgname])
            return self.defaultimg;
        return self.cache[imgname];
    }
});
