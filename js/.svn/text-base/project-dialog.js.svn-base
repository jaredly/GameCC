/** TODO: make project dialog take a 'bottons' arguemnt to the open file or some such thing. **/
var ProjectDialog = Class([], {
  id:'#project-dialog',
  __init__:function(self, parent, callbacks){
    var defaults = {
      'new':function(){},
      'delete':function(){},
      'open':function(){},
      'remove':function(){}
    };
    self.callbacks = $(defaults).extend(callbacks);
    self.parent = parent;
    self.dialog = $(self.id).dialog({
      autoOpen: false,
      height: 300,
      closeOnEscape: false,
      resizable: false,
      dialogClass: 'project',
      buttons: {
      },
      close: function () {
      },
      open: function () {
        self.listProjects();
      }
    });
    $('.buttons button.load', self.id).click(function(){
      self.load();
    });
    $('.buttons button.save', self.id).click(function(){
      self.save();
    });
    $('.buttons button.remove', self.id).click(function(){
      self.remove();
    });
    $(self.id).parent().find('.ui-dialog-titlebar-close').unbind('click').click(function(){
      $(self.id).dialog('close');
      $('#back').hide();
    });
  },
  listProjects: function (self) {
    self.parent.ajax.send('project/list_projects', {}, self._listProjects);
  },
  _listProjects: function (self, result){
    $('.project-list', self.id).html('');
    for (var i=0;i<result.projects.length;i++){
      $('<li class="project-name">'+result.projects[i]+'</li>').appendTo('.project-list', self.id).click(function(){
        $('.project-list li.selected', self.id).removeClass('selected');
        $(this).addClass('selected').parent().parent().children('input').val(this.innerHTML);
      }).dblclick(self.load);
    }
  },
  load: function(self){
    self.callbacks.open($('input.name',self.id).val());
    $(self.id).dialog('close');
    $('#back').hide();
  },
  'new': function(self){
    self.callbacks.new($('input.name', self.id).val());
    $(self.id).dialog('close');
    $('#back').hide();
  },
  open: function(self){
    $('#back').show();
    self.dialog.dialog('open');
  },
  remove: function(self){
    self.parent.ajax.send('project/remove',{project:$('input.name',self.id).val()},self.listProjects);
  },
});

