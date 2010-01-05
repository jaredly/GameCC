
var DisplayMap = Class([Display], {
    tid:'#edit-map',
    type:'map',
    grid:10,
    setup:function(self){
        $('#map-canvas .content').mousedown(function(e){
            if (e.button == 0){
                if (e.shiftKey){
                    self.addItem(e);
                    self.moving = 1;
                } else {
                    self.moving = 2;
                }
                killE(e);
            } else if (e.button == 2){
                self.moving = -1;
            }
        }).mousemove(function(e){
            if (self.moving == 1){
                self.addItem(e);
            } else if (self.moving == 2){
            }
            killE(e);
        }).mouseup(function(e){
            if (self.moving == 2){
                self.addItem(e);
            }
            self.moving = false;
            $('#map-hover').hide();
        }).bind('contextmenu',killE);

        $('#map-toolbar input').keydown(function(e){
            var inc = self.grid;
            if ($(this).hasClass('snap')) inc = 5;
            if (e.keyCode == 38){
                this.value = parseInt(this.value) + inc;
            }else if (e.keyCode == 40){
                this.value = parseInt(this.value) - inc;
            }
        }).keyup(function(e){
            self.showsize();
        }).blur(function(e){
            self.savesize();
        });
    },
    showsize:function(self) {
        var width = parseInt($('#map-toolbar .width').val());
        var height = parseInt($('#map-toolbar .height').val());
        if (!isNaN(width)){
            $('#map-canvas .content').css('width',width);
        }
        if (!isNaN(height)){
            $('#map-canvas .content').css('height',height);
        }
    },
    savesize:function(self) {
        var width = parseInt($('#map-toolbar .width').val());
        var height = parseInt($('#map-toolbar .height').val());
        width = isNaN(width)?self.object.info.width:width;
        height = isNaN(height)?self.object.info.height:height;
        self.object.set_attr('width',width);
        self.object.set_attr('height',height);
        if (!isNaN(width)){
            $('#map-canvas .content').css('width',width);
        }
        if (!isNaN(height)){
            $('#map-canvas .content').css('height',height);
        }
        var snap = parseInt($('#map-toolbar .snap').val());
        if (isNaN(snap))return;
        self.grid = snap;
        self._remake_grid();
    },
    _remake_grid:function(self) {
        var cv = $('<canvas></canvas>').hide().appendTo('body');
        var ctx = cv[0].getContext('2d');
        cv[0].width = self.grid*2;
        cv[0].height = self.grid*2;
        ctx.fillStyle = '#888888';
        ctx.fillRect(0,0,self.grid*2,self.grid*2);
        ctx.fillStyle = '#606060';
        ctx.fillRect(0,0,self.grid,self.grid);
        ctx.fillRect(self.grid,self.grid,self.grid,self.grid);
        $('#map-canvas .content').css('background-image','url('+cv[0].toDataURL()+')');
    },
    load:function(self, name){
        if (name){
            Display.load(self, name);
        }
        $('#map-canvas .content').html('');
        for (var i=0;i<self.object.info.objects.length;i++){
            var obj = self.object.info.objects[i];
            self._addItem(obj);
        }
        $('#map-objects').html('');
        for (var name in self.parent.project.data['object']){
            var div = $('<div class="object"></div>').appendTo('#map-objects')
                .css('background-image','url(' + self.parent.objScaled(name, 'small').src + ')')
                .mousedown(function(e){
                    $('#map-objects .object.selected').removeClass('selected');
                    $(this).addClass('selected');
                }).html(name).mouseover(hovershow(name)).mouseout(hoverhide);
            //div.
        }
        $('#map-objects .object').eq(0).addClass('selected');
        $('#map-canvas .content').css('width',self.object.info.width).css('height',self.object.info.height);
        $('#map-toolbar .snap').val(self.grid);
        $('#map-toolbar .width').val(self.object.info.width);
        $('#map-toolbar .height').val(self.object.info.height);
    },
    currentItem: function(self) {
        return $('#map-objects .object.selected').html();
    },
    addItem: function(self, e) {
        var pos = self.pos(e);
        var item = {x:pos.left,y:pos.top,name:self.currentItem()};
        for (var i=0;i<self.object.info.objects.length;i++){
            var obj = self.object.info.objects[i];
            if (obj.x == pos.left && obj.y == pos.top)return;
        }
        self._addItem(item);
        // change to use map asset object
        self.object.add_item(item);
    },
    pos: function(self, e) {
        var off = $('#map-canvas .content').offset();
        return {top:Math.round((e.pageY - off.top)/self.grid)*self.grid, left:Math.round((e.pageX - off.left)/self.grid)*self.grid};
    },
    _addItem: function(self, result) {
        var simg = self.parent.imagescale.objCache(result.name);
        var img = new Image();
        img.src = self.parent.objImage(result.name);
        img.className = 'item';
        img.style.left = result.x - simg.width/2 + 'px';
        img.style.top = result.y - simg.height/2 + 'px';
        var node = $(img).appendTo('#map-canvas .content');
        node.mousedown(function (e) {
            if (e.button == 0) { //

            } else if (e.button == 2) {
                self.remove(result, node);
            }
            killE(e);
        }).mousemove(function(e){
            if (e.button == 2 || self.moving == -1){
                self.remove(result, node);
            }
            killE(e);
        });
    },
    remove: function(self, item, node) {
        $(node).remove();
        self.object.remove_item(item);
    },

});

