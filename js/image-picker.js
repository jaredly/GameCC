
var ImagePicker = Class([], {
    id: '#image-picker',
    __init__: function(self, parent){
        self.parent = parent;
        self.callback;
        $('div.close', self.id).click(function (e) {
            $(self.id).hide();
            $('#back').hide();
        });
    },
    load: function(self){
        $('.images',self.id).html('');
        for (var id in self.parent.project.data['image']){
            self.limg(id);
        }
    },
    limg: function(self, id){
        var img = self.parent.project.data['image'][id];
        $('<div class="image"></div>').appendTo($('.images', self.id))
            .css('background-image','url('+self.parent.imagescale.get_scaled(img.info.subimages[0], 'medium').src+')').html(img.info.name)
            .click(function(){
                $(self.id).hide();
                $('#back').hide();
                self.callback(id);
            });
    },
    open: function(self, callback){
        self.callback = callback;
        self.load();
        $(self.id).show();
        $('#back').show();
    }
});

