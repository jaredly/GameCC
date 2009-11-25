
// var keyevents = {'letters': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'delete'], 'keypad': ['keypad_0', 'keypad_1', 'keypad_2', 'keypad_3', 'keypad_4', 'keypad_5', 'keypad_6', 'keypad_7', 'keypad_8', 'keypad_9', 'keypad_period', 'keypad_divide', 'keypad_multiply', 'keypad_minus', 'keypad_plus', 'keypad_enter', 'keypad_equals'], 'punctuation': ['backspace', 'tab', 'clear', 'return', 'pause', 'escape', 'spacebar', 'exclaim', 'quotedbl', 'hash', 'dollar', 'ampersand', 'quote', 'left_parenthesis', 'right_parenthesis', 'asterisk', 'plus_sign', 'comma', 'minus_sign', 'period', 'forward_slash', 'colon', 'semicolon', 'less_than_sign', 'equals_sign', 'greater_than_sign', 'question_mark', 'at', 'left_bracket', 'backslash', 'right_bracket', 'caret', 'underscore', 'grave'], 'arrows': ['up_arrow', 'down_arrow', 'right_arrow', 'left_arrow'], 'numbers': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 'special': ['insert', 'home', 'end', 'page_up', 'page_down', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'numlock', 'capslock', 'scrollock', 'right_shift', 'left_shift', 'right_ctrl', 'left_ctrl', 'right_alt', 'left_alt', 'right_meta', 'left_meta', 'left_windows_key', 'right_windows_key', 'mode_shift', 'help', 'print_screen', 'sysrq', 'break', 'menu', 'power', 'euro']};

var keynames = {8: 'backspace', 9: 'tab', 13: 'enter', 16: 'shift', 17: 'control', 19: 'pause_break', 20: 'caps_lock', 27: 'esc', 32: 'spacebar', 33: 'page_up', 34: 'page_down', 35: 'end', 36: 'home', 37: 'left_arrow', 38: 'up_arrow', 39: 'right_arrow', 40: 'down_arrow', 45: 'insert', 46: 'delete', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e', 70: 'f', 71: 'g', 72: 'h', 73: 'i', 74: 'j', 75: 'k', 76: 'l', 77: 'm', 78: 'n', 79: 'o', 80: 'p', 81: 'q', 82: 'r', 83: 's', 84: 't', 85: 'u', 86: 'v', 87: 'w', 88: 'x', 89: 'y', 90: 'z', 96: 'numpad_0', 97: 'numpad_1', 98: 'numpad_2', 99: 'numpad_3', 100: 'numpad_4', 101: 'numpad_5', 102: 'numpad_6', 103: 'numpad_7', 104: 'numpad_8', 105: 'numpad_9', 106: 'multiply', 107: 'add', 109: 'subtract', 110: 'decimal', 111: 'divide', 112: 'f1', 113: 'f2', 114: 'f3', 115: 'f4', 116: 'f5', 117: 'f6', 118: 'f7', 119: 'f8', 120: 'f9', 122: 'f11', 123: 'f12', 124: 'f13', 125: 'f14', 126: 'f15', 144: 'num_lock', 145: 'scrlk'}
var keyvalues = [];
for (var i in keynames){
  keyvalues.push(keynames[i]);
}

function humanize(x){
  return x.replace(/_/g,' ').replace(/-/g,' ').replace(/(^| )\w/g, function(x){return x.toUpperCase();});
}

/** checked, good **/

var EventPicker = Class([], {
  id:'#event-picker',
  others : [
    'create',
    'created',
    'destroy',
    'collide',
    'timer',
    'step',
    'draw',
    'move',
    'mouse_up',
    'mouse_down',
    'mouse_move',
    'key_down',
    'key_press',
    'key_release',
    'off_of_map',
    'map_start',
    'map_end',
    'game_start',
    'game_end',
  ],
  __init__:function(self, parent, options){
    var defaults = {
      onSubmit:function(){},
      onCancel:function(){}
    }
    self.parent = parent;
    self.options = $.extend(defaults,options);
    self.disabled = false;
    $(self.id).html('<div class="delete"></div>');
    $('.delete',self.id).click(self.hide);
    for (var i=0;i<self.others.length;i++){
      $.data($('<li class="event-type">'+humanize(self.others[i])+'</li>').appendTo(self.id)[0], 'name', self.others[i]);
    }
    // select event
    $('li.event-type').click(function(e){
      var name = $.data(this, 'name');
      // collision dropdown
      if (name === 'collide'){
        var items = [];
        for (var name in self.parent.project.data['object']){
          items.push([name,self.metaevent('collide_'+name)]);
        }
        return contextMenu(items)(e);
      }else if (name.indexOf('key')===0){ // key event
        return keyMenu(e,function(e){
          if (e){self.metaevent(name+'_'+e)();}
          else{self.metaevent(name)();}
        });
      }else if (name === 'timer'){
        var items = [];
        for (var i=0;i<10;i++){
          items.push(['Timer '+i,self.metaevent('timer_'+i)]);
        }
        return contextMenu(items)(e);
      }
      self.options.onSubmit(name);
      self.hide();
    });
  },
  show:function(self,tmpsub,title){
    if (tmpsub && typeof(tmpsub)==='function') {
      var old = self.options.onSubmit;
      self.options.onSubmit = function(name){
        tmpsub(name);
        self.options.onSubmit = old;
      };
    }
    $('.title',self.id).html(title?title:'Choose an Event');
    $('#back,'+self.id).show();
  },
  hide:function(self){
    $('#back,'+self.id).hide();
  },
  metaevent:function(self, name){
    return function(){
      self.options.onSubmit(name);
      self.hide();
    };
  }
});

