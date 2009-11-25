
/**
  id, onchange, rightclick
  add('name',true/false);
  
 **/
var TabManSingle = Class([], {
  __init__: function(self, id, onchange, rightclick){
    self.id = id;
    self.tabs = {};
    self.onchange = onchange || function(){};
    self.rightclick = rightclick || function(){};
    self.selected = '';
  },
  add: function(self, name, switchto){
    self.tabs[name] = $('<div class="handle">' + humanize(name) + '</div>').appendTo(self.id).click(function(e){
      var name = $.data(this, 'name');
      self.onchange(self.selected, name);
      self.selected = name;
      $('div.handle', self.id).removeClass('selected');
      $(this).addClass('selected');
    }).bind('contextmenu',function(e){
      self.rightclick(e, $.data(this, 'name'));
      return killE(e);
    });
    $.data(self.tabs[name][0], 'name', name);
    if (switchto || !self.selected)
      self.tabs[name].click();
  },
  remove: function(self, name){
    $(self.tabs[name]).remove();
    delete self.tabs[name];
    if (name == self.selected){
      self.selected = '';
      self.onchange(name,'');
    }
  },
  change: function(self, from, to){
    self.tabs[from].html(to);
    $.data(self.tabs[from][0],'name',to);
    self.tabs[to] = self.tabs[from];
    delete self.tabs[from];
  },
  clear: function(self){
    $(self.id).html('');
    self.selected = '';
  }
});

var DisplayObject = Class([Display], {
  tid:'#edit-object',
  type:'object',
  setup: function(self){
    self.EP = EventPicker(self.parent,{onSubmit:self.addEvent});
    $('#object-image').click(function(){
      self.parent.imagepicker.open(self.changeImage);
    });
    self.events = TabManSingle('#object-events .contents', self.selectEvent, self.eventCM);
    $('#object-parent').change(function(){
      self.object.set_attr('parent',this.value);
    });
    
    $('#object-event-toolbar .add').click(self.EP.show);
    $('#object-event-toolbar .remove').click(self.removeEvent);
    $('#object-actions').sortable({
      stop:function(){
        self.saveActions();
      },
      axis:'y'
    }).droppable({
      hoverClass:'hover',
      accept:'div.plugin-image',
      drop:function(event, ui){
        if (!self.events.selected)return;
        if (ui.draggable.hasClass('action') || !ui.draggable.hasClass('plugin-image'))return;
        //if (event.originalTarget.id!==object-actions)return;
        var off = $('#object-actions').offset();
        if (ui.draggable.hasClass('conditional')){
          var node = self.parent.plugins.plugins['if'].drop([event.pageX-off.left, event.pageY-off.top]);
          self.parent.plugins.plugins['endif'].drop([event.pageX-off.left, event.pageY-off.top+30]);
          var name = $.data(ui.draggable[0],'name');
          
          var sub = $('.subaction.sub-expression',node);
          
          var data = $.data(node[0],'data');
          var plugin = self.parent.plugins.plugins[$.data(ui.draggable[0],'name')];
          ui.helper.remove();
          
          plugin.showForm(sub, {}, function(form,sub){
            var data = $.data(node[0],'data');
            data['expression'] = {};
            data['expression'].name = plugin.info.name;
            data['expression'].data = plugin.getData(form);
            var unhover = $.data(sub[0],'unhover');
            unhover();
            unhover = hovertext(sub,plugin.text(data['expression'].data));
            $.data(sub[0],'unhover',unhover);
            $.data(node[0],'data',data);
            //debugger;
            plugin.bgicon(sub,true);
            self.saveActions();
          });
        }else{
          $.data(ui.draggable[0],'ondrop')([event.pageX-off.left, event.pageY-off.top]);
          ui.helper.remove();
          if (ui.draggable.is('.'+['if','and','or','while','with','repeat'].join(',.'))){
            self.parent.plugins.plugins['endif'].drop([event.pageX-off.left, event.pageY-off.top+30]);
          }
        }
      }
    });
    $('#object-actions').droppable('disable');
    
  },
  load:function(self, name) {
    if (name){
      Display.load(self, name);
    }
    if (!self.object.info.image || !self.parent.project.data['image'][self.object.info.image] || !self.parent.project.data['image'][self.object.info.image].info.subimages.length){
      
    } else {
      var io = self.parent.project.data['image'][self.object.info.image].info.subimages[0];
      var img = self.parent.imagescale.get_scaled(io, 'large');
      $('#object-image').css('background-image', 'url('+img.src+')');
    }
    self.load_parents();
    
    self.load_events();
    self.load_actions();
  },
  load_parents: function(self){
    $('#object-parent').html('<option value="BaseObject">BaseObject</option>');
    for (var name in self.parent.project.data['object']){
      $('<option value="'+name+'">'+name+'</option>').appendTo('#object-parent');
    }
    $('#object-parent').val(self.object.info.parent);
  },
  load_events: function(self){
    self.events.clear();
    for (var name in self.object.info.events){
      self.events.add(name);
    }
  },
  load_actions: function(self,selected){
    $('#object-actions').html('');
    selected = selected || self.events.selected;
    if (!selected) return;
    for (var i=0;i<self.object.info.events[selected].length;i++){
      self.addAction.apply(self,self.object.info.events[selected][i])
    }
  },
  addAction:function(self,name,data){
    if (!data){
      throw "invalid";
    }
    if (!self.parent.plugins.plugins[name]){
      if (confirm('invalid action '+name+' found. delete?')){
        return;
      }
    }
    self.parent.plugins.plugins[name].addAction(data);
  },
  newAction:function(self,name,data){
    self.addAction(name,data);
    self.saveActions();
  },
  saveActions: function(self) {
    if (!self.events.selected)throw "no selected event?";
    var actions = [];
    $('#object-actions div.action').each(function(){
      var data = $.data(this, 'data');
      data['disabled'] = $(this).find('div.disable input').attr('checked');
      actions.push([$.data(this, 'name'), data]);
    });
    self.object.save_actions(self.events.selected, actions);
  },
  addEvent: function(self, name) {
    if (self.object.add_event(name)) {
      self.events.add(name, true);
    }
  },
  removeEvent: function(self) {
    if (self.object.remove_event(self.events.selected)) {
      self.events.remove(self.events.selected);
    }
  },
  eventCM: function(self, event, name) {
    contextMenu([['Change Event',self.change_event(name)],
      ['Duplicate Event',self.duplicate_event(name)],
      ['Delete Event',self.remove_event(name)]])(event);
  },
  change_event:function(self, name) {
    return function(){
      self.EP.show(function(to){
        self.object.change_event(name, to);
        self.events.change(name,to);
      },'Change To');
    };
  },
  duplicate_event:function(self, name) {
    return function(){
      self.EP.show(function(to){
        self.object.duplicate_event(name, to, function(){
          self.events.add(to,true);
        });
      },'Duplicate Event');
    };
  },
  remove_event:function(self, name) {
    return function(){
      self.object.remove_event(name);
      self.events.remove(name);
    };
  },
  selectEvent: function(self,from,to) {
    $('#object-actions').droppable('enable');
    self.load_actions(to);
  },
  unload:function(self){
    Display.unload(self);
    $('#object-image').css('background-image', '');
    self.events.clear();
    $('#object-actions').html('');
  },
  changeImage:function(self, name){
    self.object.set_attr('image', name, function(){self.load();});
    $('.name input',self.tid).focus().select();
  },
});
