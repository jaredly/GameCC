


var MediaLibrary = Class([], {
  id: '#media-library',
  __init__: function(self, parent){
    self.parent = parent;
    self.callback;
    $('div.close', self.id).click(function (e) {
      $(self.id).hide();
      $('#back').hide();
    });
    var button = $('button.upload',self.id);
    self.ab = new AjaxUpload(button,{
        action: 'cgi/index.py',
        name: 'file',
        data: {'cmd':'project/uploadimage'},
        onSubmit : function (file, ext) {
            self.ab._settings.data.project = self.parent.project.info.name;
            button.text('Uploading');
            this.disable();
        },
        onComplete: function (file, response) {
            button.text('Upload');
            this.enable();
            self.parent.imagescale.load(response,self.onlimg);
        }
    });
    self.importing = false;
    $('button.import',self.id).click(function(){
      self.switchToImport();
    });
    $('button.import-selected,button.ccancel',self.id).hide();
    $('button.import-selected',self.id).click(function(){
      self.doImport();
    });
    $('button.ccancel',self.id).click(function(){
      self.cancelImport();
    });
  },
  show_loading:function(self){
    $('.loading,.back',self.id).show();
  },
  done_loading:function(self){
    $('.loading,.back',self.id).hide();
  },
  switchToImport:function(self){
    $('button.import-selected,button.ccancel',self.id).show();
    $('button.upload,button.url,button.import',self.id).hide();
    $('.images',self.id).html('');
    self.importing = true;
    self.parent.ajax.send('project/list_all_images',{},function(results) {
      for (var i=0; i<results.images.length; i++){
        self.parent.imagescale.load(results.images[i],self.onlimg);;
      }
    });
  },
  doImport:function(self){
    var images = [];
    $('.images .image.selected',self.id).each(function(){
      images.push($.data(this,'image'));
    });
    self.show_loading();
    self.parent.project.add_images(images,self.reload);
    $('button.import-selected,button.ccancel',self.id).hide();
    $('button.upload,button.url,button.import',self.id).show();
    self.reload();
  },
  cancelImport:function(self){
    $('button.import-selected,button.ccancel',self.id).hide();
    $('button.upload,button.url,button.import',self.id).show();
    self.reload();
  },
  load: function(self, images){
    self.done_loading();
    $('.images',self.id).html('');
    for (var i=0; i<images.length; i++){
      self.parent.imagescale.load(images[i], self.onlimg);
      self.parent.ajax.increment();
    }
  },
  reload: function(self){
    $('.images',self.id).html('');
    self.importing = false;
    self.parent.ajax.send('project/list_images',{},function (results) {
      self.load(results.images);
    });
  },
  onlimg: function(self, name){
    var img = self.parent.imagescale.get_scaled(name, 'medium');
    var div = $('<div class="image"></div>').appendTo($('.images', self.id))
      .css('background-image','url('+img.src+')').html(name+'<br/>'+img.owidth+'x'+img.oheight)
      .click(function(){
        if (self.importing){
          $(this).toggleClass('selected');
        }else{
          $(self.id).hide();
          $('#back').hide();
          self.callback(name);
        }
      });
    $.data(div[0],'image',name);
  },
  open: function(self, callback){
    self.callback = callback;
    $(self.id).show();
    $('#back').show();
  }
});
