
/* this fixes the problem of having multiple elements with the same id
 * -- usually ui tabs requires the tab body elements to be identified by id
 * this allows them to be identified by class, by making the href be #.class as opposed to #id (notice the dot)*/
jQuery.ui.tabs.prototype = jQuery.extend(jQuery.ui.tabs.prototype, {
    _sanitizeSelector: function (hash) {
        if (hash[1] === '.') {
            hash = hash.slice(1);
        }
        else {
            return hash.replace(/:/g, '\\:');
        }
        var pelem = this.element;
        while (!pelem.is('.multivalueable')) {
            pelem = pelem.parent();
        }
        return jQuery(hash.replace(/:/g, '\\:'), pelem); // we need this because an id may contain a ":"
    }
});

function obj_extend(a,b){
    var c={};
    for (x in a)c[x]=a[x];
    for (x in b)c[x]=b[x];
    return c;
}

var subtypes = {};

var SubType = Class([], {
    type:null,
    defaults:{value:''},
    __init__:function(self, input, options) {
        self.settings = obj_extend(self.defaults, options);
        self._value = self.settings.value;
        self.tip = input.after('<div class="subtype-tip '+self.type+'"></div>');
        self.input = input;
        self.init();
    },
    init:function(self) {},
    value:function(self) {
        return self._value;
    },
    refresh:function(self) {
        self.input.val(self._value);
    },
    show:function(self) { self.refresh(); },
    hide:function(self) { self.hidetip(); },
    mdown:function(self, e) {},
    mup:function(self, e) {},
    click:function(self, e) {
        self.tip.toggleSlide();
    },
    showtip:function(self) {
        self.tip.show();
    },
    hidetip:function(self) {
        self.tip.hide();
    }
});

subtypes['bool'] = Class([SubType], {
    type:'bool',
    defaults:{'value':true},
    click:function(self) {
        self._value = !self._value;
        self.refresh();
    }
});

subtypes['default'] = Class([SubType], {
    type:'default',
    defaults:{'value':''},
    value:function(self){return self.input.val();}
});

// value: [subtype, val]

var SuperType = Class([], {
    subtypes:[],
    type:'',
    __init__:function(self, div, input, value) {
        self.div = div;
        self.input = input;
        self.input.mousedown(self.mdown);
        self.input.mouseup(self.mup);
        self.input.click(self.click);
        self.input.addClass('super-'+self.type);
        self._current = value?value[0]:self.subtypes[0][0];
        self.div.addClass('sub-'+self._current);
        self.subs = {};
        for (var i=0;i<self.subtypes.length;i++){
            if (!subtypes[self.subtypes[i][0]])
                subtypes[self.subtypes[i][0]] = subtypes['default'];
            var obj = subtypes[self.subtypes[i][0]](self.input, self.subtypes[i].slice(1));
            self.subs[self.subtypes[i][0]] = obj;
        }
        if (value){
            self.subs[self._current].setValue(value[1]);
        }
        self.subs[self._current].show();
    },
    value:function(){
        return [self._current, self.subs[self._current].value()];
    },
    mdown:function(self, e){
        return self.subs[self._current].mdown(e);
    },
    mup:function(self, e){
        return self.subs[self._current].mup(e);
    },
    click:function(self, e){
        return self.subs[self._current].click(e);
    },
    change_sub:function(self, to) {
        if (to == self._current)return;
        self.subs[self._current].hide();
        self.div.removeClass('sub-'+self._current);
        self._current = to;
        self.div.addClass('sub-'+self._current);
        self.subs[self._current].show();
    }
});

var supertypes = {};
// add a random...[function] to instance
supertypes['instance'] = Class([SuperType], {
    subtypes: [['variable','object-instance']],
});

supertypes['objecttype'] = Class([SuperType], {
    subtypes: [['objecttype'],
               ['variable','object-type']],
});

supertypes['pos'] = Class([SuperType], {
    subtypes: [['number',{min:0,max:100}],
               ['variable',{type:'float'}],
               ['function',{type:'float'}]],
});

supertypes['bool'] = Class([SuperType], {
    subtypes: [['bool'], ['variable','bool'], ['function',{type:'bool'}]],
});

supertypes['direction'] = Class([SuperType], {
    subtypes: [['number',{min:0,max:360}],
               ['variable',{type:'float'}],
               ['dirpad']],
});

supertypes['speed'] = Class([SuperType], {
    subtypes: [['number',{min:0,max:10}],
               ['variable',{type:'float'}],
               ['function',{type:'float'}]],
});










/**

var InputType = Class([], {
    name:'example',
    title:'Example',
    __init__:function(self, parent, div, value){
        self.div = div;
    },
    value:function(){
        return null;
    }
});

/**

number, select, select string, object, direction, percent, key, bool, not, random, randint, variable, timer, custom, string

**

var InputTypes = {};

InputTypes['number'] = Class([InputType], {
    title:'Number',
    __init__:function(self, parent, div, value, full){
        var min,max,step;
        if (typeof(full)!=='string' && full && full.length){
            min = full.length>1?full[1]:0;
            max = full.length>2?full[2]:100;
            step = full.length>3?full[3]:1;
        }
        self.step = step;
        self.div = div;

        value = self.validate(value);

        self.node = $('<div class="number-left"></div>').appendTo(div).html(value);
        self.negative = value < 0;
        self._value = value;//!isNaN(parseFloat(value)) && parseFloat(value) || 0;
        var neg = $('<div class="number-np">+/-</div>').appendTo(div);
        neg.click(function(){
            self.negative = !self.negative;
            self.update();
        });
        var slider = $('<div class="number-slider"></div>').appendTo(div);
        slider.slider({
            value:Math.abs(value),
            slide:function(e, ui){
                self.update(ui.value);
            },
            min:min || 0,
            max:max || 100,
            step:step||1
        });
    },
    update:function(self, value){
        if (typeof(value)==='undefined') {
            value = self._value;
        }
        self._value = [1,-1][self.negative?1:0] * Math.abs(value);
        self.node.html(self._value.toFixed((self.step+'').slice((self.step+'').indexOf('.')).slice(1).length));
    },
    value:function(self){
        return self._value;
    },
    validate:function(self, value) {
        value = parseFloat(value);
        if (isNaN(value))return 0;
        return value;
    }
});

InputTypes['select'] = Class([InputType], {
    title:'Select',
    __init__:function(self, parent, div, value, full) {
        self.parent = parent;
        self.div = div;
        self.select = $('<select></select>').appendTo(div);
        var args = [];
        if (typeof(full) !== 'string'){
            args = full.slice(1);
        }
        self.args = args;
        for (var i=0;i<args.length;i++) {
            self.select.append('<option>' + args[i] + '</option>');
        }
        if (value){
            self.select.val(value);
        }
    },
    value:function(self) {
        return self.select.val();
    }
});

InputTypes['select string'] = Class([InputTypes['select']], {
    title:'Select a string'
});

InputTypes['object'] = Class([InputType], {
    title:'Object',
    __init__:function(self,parent, div, value){
        self.parent = parent;
        self.div = div;
        self.sel = $('<select><option>BaseObject</option></select>').appendTo(div);
        for (var name in parent.parent.project.data['object']){
            self.sel.append('<option>'+name+'</option>');
        }
        self.sel.val(value);
    },
    value:function(self) {
        return self.sel.val();
    }
});

InputTypes['direction'] = Class([InputType], {
    title:'Direction',
    __init__:function(self, parent, div, value){
        self.div = div;
        self.div.direction({value:self.validate(value)});
    },
    value:function(self){
        return self.div.direction('value');
    },
    validate:function(self, value) {
        value = parseFloat(value);
        if (isNaN(value))return 0;
        return value;
    }
});

InputTypes['percent'] = Class([InputTypes['number']], {
    title:'Percent',
    __init__:function(self, parent, div, value){
        InputTypes['number'].__init__(self, parent, div, value, 0, 100);
        self.update();
    },
    update:function(self, value){
        if (typeof(value)==='undefined') {
            value = self._value;
        }
        self._value = [1,-1][self.negative?1:0] * Math.abs(value);
        self.node.html(self._value + '%');
    },
    value:function(self){
        return self._value;
    },
    validate:function(self, value) {
        value = parseFloat(value);
        if (isNaN(value))return 0;
        return value;
    }
});

InputTypes['key'] = Class([InputType], {
    name:'key',
    title:'Key',
    __init__:function(self, parent, div, value){
        self.div = div;
        self.input = $('<input class="key"/>').appendTo(div).val(value);
        self.input.keydown(function(e){
            this.value = keynames[e.keyCode];
            e.stopPropagation();
            e.preventDefault();
            return false;
        });
    },
    value:function(self){
        return self.input.val();
    },
    validate:function(self, value) {
        if (keyvalues.indexOf(value) !== -1){
            return value;
        }
        return 0;
    }
});

InputTypes['bool'] = Class([InputType], {
    title:'Boolean',
    __init__:function(self, parent, div, value){
        self.div = div;
        self.node = $('<div class="bool-toggle"></div>').appendTo(div).html((value === true)+'');
        self.node.click(self._switch);
    },
    _switch: function(self) {
        if (self.node.html()=='true'){
            self.node.html('false');
        }else{
            self.node.html('true');
        }
    },
    value:function(self) {
        return self.node.html() == 'true';
    },
    validate:function(self, value) {
        return value === true;
    }
});

InputTypes['not'] = Class([InputType], {
    title:'Not',
    __init__:function(self, parent, div, value, full) {
        self.div = div;
        //debugger;
        self.node = $('<input type="checkbox"/>').appendTo(div);
        self.node[0].checked = value===true;
        $('<span>NOT</span>').appendTo(div);
        self.div.click(self._switch);
    },
    _switch:function(self,e) {
        if ($(e.target).is('input')) return;
        self.node[0].checked = !self.node[0].checked;
    },
    value:function(self) {
        return self.node[0].checked;
    },
    validate:function(self, value) {
        return value === true;
    }
});

InputTypes['random'] = Class([InputType], {
    title:'Random',
    __init__:function(self, parent, div, value, full){
        self.div = div;
        $('<span>pick a random number from</span>').appendTo(div);
        self.min = $('<input class="number"/>').appendTo(div);
        $('<span> to </span>').appendTo(div);
        self.max = $('<input class="number">').appendTo(div);
        value = self.validate(value);
        if (value[0]==0 && value[1]==0 && typeof(full)!=='string' && full && full.length>1){
                if (full.length == 2)value = [0,full[1]];
                else if (full.length == 3)value = full.slice(1);
        }
        self.min.val(value[0]);
        self.max.val(value[1]);
    },
    value:function(self){
        return [self.min.val(), self.max.val()];
    },
    validate:function(self,value) {
        if (!value || !value.length === 2)return [0,0];
        return value;
    },
});

InputTypes['randint'] = Class([InputTypes['random']], {
    title:'RandInt',
    value:function(self){
        return [self.min.val(),self.max.val()];
    }
});

var allowedvariables = {
    'self':    ['vspeed','hspeed','speed','direction','x','y','rotation','opacity','gdirection','gspeed','imagepos','imagespeed'],
    'other': ['vspeed','hspeed','speed','direction','x','y','rotation','opacity','gdirection','gspeed','imagepos','imagespeed'],
    'object':['vspeed','hspeed','speed','direction','x','y','rotation','opacity','gdirection','gspeed','imagepos','imagespeed'],
    'game':    ['mousex','mousey']};

InputTypes['variable'] = Class([InputType], {
    title:'Variable',
    __init__:function(self, parent, div, value){
        self.who = $('<select><option>self</option><option>other</option><option>object</option><option>game</option></select>').appendTo(div);
        self.sel = $('<select></select>').appendTo(div);
        if (value && value.length === 2) {
            var parts = value;
            self.who.val(parts[0]);
            self.reload();
            self.sel.val(parts[1]);
        }else{
            self.reload();
        }
        self.who.change(self.reload);
    },
    reload:function(self) {
        self.sel.html('');
        for (var i=0;i<allowedvariables[self.who.val()].length;i++){
            self.sel.append('<option>'+allowedvariables[self.who.val()][i]+'</option>');
        }
    },
    value:function(self){
        return [self.who.val(), self.sel.val()];
    }
});

InputTypes['timer'] = Class([InputTypes['number']], {
    title:'Timer',
    __init__:function(self, parent, div, value){
        InputTypes['number'].__init__(self, parent, div, value, ['number', 0, 10, 1]);
    }
});

InputTypes['custom'] = Class([InputType], {
    title:'Custom',
    __init__:function(self, parent, div, value) {
        self.parent = parent;
        self.div = div;
        self.inp = $('<input type="text"/>').appendTo(div).val(self.validate(value) || '');
    },
    value:function(self) {
        return self.inp.val();
    },
    validate:function(self,value) {
        return value;
    }
});

InputTypes['string'] = Class([InputTypes['custom']], {
    title:'String',
    value:function(self) {
        return "'" + InputTypes['custom'].value(self).replace(/\\/g,'\\\\').replace(/'/g,"\\'") + "'";
    },
    validate:function(self,value) {
        if (typeof(value)!=='string')return value + '';
        if (value[0]=="'")value=value.slice(1);
        if (value.slice(-1)=="'")value=value.slice(0,-1)
        return value;
    }
});

var MultiValuable = Class([],{
    template:'<div class="multivalueable"><div class="tabdiv"><ul class="tab-titles"></ul></div><div class="contents"></div><div class="buttons"></div></div>',
    __init__:function(self, parent, node, types, value, update) {
        self.parent = parent;
        self.node = node;
        self.update = update;

        types.push('custom');

        self._inputs = {};
        /***
        var first = value && value[0] || null;
        for (var i=0;i<types.length;i++) {
            var type = types[i];
            if (typeof(type) !== 'string')
                type = type[0];
            var div = $('<div class="input-type type-' + type + '"></div>').appendTo(self.node).hide();
            self._inputs[type] = InputTypes[type](parent, div, value && value[1], types[i]);
            self._inputs[type].div = div;
        }
        if (!first){
            first = types[0];
            if (typeof(first) !== 'string'){
                first = first[0];
            }
        }


        self.types = types;
        self._inputs[first].div.show();
        $('<div class="expand-button"></div>').appendTo(node).click(self.showhide);
        $('li.tab-'+first).hide();

        self.current = first;
    },
    showhide: function(self, e) {
        var items = [];//[self.current,function(){},true]];
        for (var i=0;i<self.types.length;i++) {
            var type = self.types[i];
            if (typeof(type) !== 'string')
                type = type[0];
            if (type == self.current){
                items.push([type, function(){}, true]);
            } else {
                items.push([type, self.switchTo(type)]);
            }
        }
        contextMenu(items)(e);
    },
    switchTo: function(self, type) {
        return function(){
            self._inputs[self.current].div.hide()
            // look into value transfer
            self.current = type;
            self._inputs[self.current].div.show();
            self.update();
        }
    },
    value:function(self) {
        return [self.current,self._inputs[self.current].value()];
    }
});

**/
