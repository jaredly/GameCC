
var DisplayImage = Class([Display], {
  tid:'#edit-image',
  type:'image',
  setup:function(self){
    $('#edit-image-preview').click(function(){
      self.parent.media.open(self.changeImage);
    });
    $('#image-toolbar .add').click(function(){
      self.parent.media.open(self.addImage);
    });
    $('#image-toolbar .remove').click(function(){
      var seld = $('#edit-image-list .image.selected');
      if (!seld.length)return;
      seld.remove();
      self.save_images();
    });
  },
  load:function(self, name) {
    // load name
    if (name){
      Display.load(self, name);
    }
    
    // load subimages
    $('#edit-image-list').html('');
    if (!self.object.info.subimages.length)
      return;
    var img = self.parent.imagescale.get_scaled(self.object.info.subimages[0], 'large');
    $('#edit-image-preview').css('background-image', 'url('+img.src+')');
    for (var i=0;i<self.object.info.subimages.length;i++) {
      var img = self.parent.imagescale.get_scaled(self.object.info.subimages[i], 'medium');
      var div = $('<div class="image"></div>').appendTo('#edit-image-list')
        .css('background-image','url('+img.src+')').click(function () {
          $('#edit-image-list .image.selected').removeClass('selected');
          $(this).addClass('selected');
        }).html(img.oheight + ' x ' + img.owidth);
      $.data(div[0],'image',self.object.info.subimages[i]);
    }
    
    // load speed
    $('#edit-image-speed').val(self.object.info.speed).blur(function(){
      var val = parseFloat(this.value);
      val = isNaN(val)?1:val;
      this.value = val;
      self.object.set_attr('speed',val);
    });
  },
  unload:function(self){
    Display.unload(self);
    $('#edit-image-preview').css('background-image', '');
    $('#edit-image-list').html('');
  },
  changeImage:function(self,name){
    self.object.set_images([name],self.load);
    $('.name input',self.tid).focus().select();
  },
  addImage:function(self,name){
    self.object.add_image(name, self.load);
  },
  save_images:function(self) {
    var subimages = [];
    $('#edit-image-list .image').each(function(){
      subimages.push($.data(this,'image'));
    });
    self.object.set_images(subimages,self.load);
  }
});
