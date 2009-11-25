
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
    for (var name in self.parent.project.data['image']){
      self.limg(name);
    }
  },
  limg: function(self, name){
    $('<div class="image"></div>').appendTo($('.images', self.id))
      .css('background-image','url('+self.parent.imagescale.get_scaled(self.parent.project.data['image'][name].info.subimages[0], 'medium').src+')').html(name)
      .click(function(){
        $(self.id).hide();
        $('#back').hide();
        self.callback(name);
      });
  },
  open: function(self, callback){
    self.callback = callback;
    self.load();
    $(self.id).show();
    $('#back').show();
  }
});

