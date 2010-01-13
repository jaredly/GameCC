
var Plugin = Class([], {
    popsup:true,
    droppos:null,
    __init__:function(self, parent, info){
        self.parent = parent;
        self.info = info;
        if (self.info.type == 'conditional'){
            self.info.inputs['not'] = 'not';
        }
        self.nid = '#plugin-'+info.name;
        self._make_li();
        hovertext(self.li, self.info.description);
        self.bgicon(self.li,true);
        $.data(self.li[0], 'ondrop', self.drop);
        $.data(self.li[0], 'name', self.info.name);
    },

    _make_li : function(self){
        self.li = $('<div id="plugin-'+self.info.name+'" class="plugin-image '+self.info.type+' '+self.info.name+'"></div>')
            .appendTo(self.parent.id)
            .draggable({helper:'clone',
                drag:function(event, ui){
                    var off = $(self.parent.actions).offset();
                    var aty = parseInt((event.pageY - off.top)/40);
                    var node = $('li.action',self.parent.actions).removeClass('drophover').eq(aty);
                    node.addClass('drophover');
                }});
    },
    text:function(self, data){
        var text = self.info.text.replace('<','&lt;').replace('>','&gt;');
        var empty = true;
        for (var key in data){
            empty = false;
            /** TODO fix for new action [type, data] **/
            var value = data[key][1];
            if (self.info.inputs[key]==='float' && !isNaN(parseInt(value))){
                value = (''+value).slice(0,5);
            }else if (self.info.inputs[key]==='vector'){
                value = '(' + (''+value[0]).slice(0,5) + ', ' + (''+value[1]).slice(0,5) + ')';
            }else if (self.info.inputs[key]==='conditional'){
                value = '<div class="subaction sub-'+key+'"></div>';
            }
            var tfrx = new RegExp('\\{'+key+'\\?([^:]*):([^\\}]*)\\}','g')
            if (value === true){
                text = text.replace(tfrx, '$1');
            } else if (value === false){
                text = text.replace(tfrx, '$2');
            } else {
                text = text.replace(new RegExp('\\{'+key+'\\}','g'), value);
            }
        }
        if (empty){
            for (var key in self.info.inputs){
                if (self.info.inputs[key]==='conditional'){
                    value = '<div class="subaction sub-'+key+'"></div>';
                    text = text.replace(new RegExp('\\{'+key+'\\}','g'), value);
                }
            }
        }
        return text;
    },

    drop:function(self, pos){
        self.droppos = pos;
        return self.showForm();
    },
    icon:function(self){
        if (self.info.icon.indexOf(',')===-1){
            return self.info.icon;
        }
    },

    bgicon:function(self,node,small){
        if (self.info.icon.indexOf(',') === -1){
            node.css('background-image', 'url(images/plugins/'+self.info.icon+')');
        }else{
            var parts = self.info.icon.split(',');
            if (small)parts[0]='allplugins-small.png';
            node.css('background-image', 'url(images/plugins/'+parts[0]+')');
            node.css('background-position', (1 - parseInt(parts[1])*(small?33:65))+'px ' + (1 - parseInt(parts[2])*(small?33:65))+'px')
        }
    },
    setupSub:function(self, node){
    },
    addAction:function(self, data){
        try{
            var node = $('<div class="action '+self.info.type+' '+self.info.name+'"><div class="icon"></div><div class="text"></div><div class="disable"><input type="checkbox" title="disable"/></div><div class="delete"></div></div>').appendTo(self.parent.actions);
        }catch(e){
            debugger;
        }
        node.dblclick(function(){self.showForm(node);});
        node.bind('contextmenu',function(e){self.showForm(node);killE(e);});
        node.find('div.text').html(self.text(data));
        self.bgicon(node.find('div.icon'),true);
        $.data(node[0],'name',self.info.name);
        $.data(node[0],'data',data);
        for (var name in self.info.inputs){
            (function(name){
                // refactor....
                var type = self.info.inputs[name];
                if (type!=='conditional')
                    return;
                var sub = $('div.text .sub-'+name,node);
                var unhover;
                if (data[name] && data[name].name){
                    unhover = hovertext(sub,self.parent.plugins[data[name].name].text(data[name].data));
                }else{
                    unhover = hovertext(sub,'drag and drop to add a conditional');
                }
                sub.find('.delete').click(function(){
                    var data = $.data(node[0],'data');
                    data[name] = {};
                    $.data(node[0],'data',data);
                    var unhover = $.data(sub[0],'unhover');
                    unhover();
                    unhover = hovertext(sub,'drag and drop to add a conditional');
                    $.data(sub[0],'unhover',unhover);
                    sub.css('background-image','');
                });
                sub.dblclick(function(){
                    if (!data[name].name)return;
                    var plugin = self.parent.plugins[data[name].name];
                    plugin.showForm(sub, data[name].data, function(form,sub){
                        var data = $.data(node[0],'data');
                        data[name].data = plugin.getData(form);
                        $.data(node[0],'data',data);
                        self.parent.parent.display['object'].saveActions();
                        var unhover = $.data(sub[0],'unhover');
                        unhover();
                        unhover = hovertext(sub,plugin.text(data[name].data));
                        $.data(sub[0],'unhover',unhover);
                    });
                });
                sub.droppable({
                    accept:'div.conditional',
                    tolerance:'touch',
                    hoverClass:'hover',
                    greedy:true,
                    drop:function(event, ui){
                        event.stopPropagation();
                        event.preventDefault();
                        var data = $.data(node[0],'data');
                        var plugin = self.parent.plugins[$.data(ui.draggable[0],'name')];
                        ui.helper.remove();
                        plugin.showForm(sub, {}, function(form,sub){
                            var data = $.data(node[0],'data');
                            data[name] = {};
                            data[name].name = plugin.info.name;
                            data[name].data = plugin.getData(form);
                            unhover();
                            unhover = hovertext(sub, plugin.text(data[name].data));
                            $.data(node[0],'data',data);
                            //debugger;
                            plugin.bgicon(sub,true);
                            self.parent.parent.display['object'].saveActions();
                        });
                        return false;
                    }
                });
                $.data(sub[0],'unhover',unhover);
                if (data[name] && data[name].name){
                    self.parent.plugins[data[name].name].bgicon(sub,true);
                }else{
                    data[name] = {};
                }
            }(name));
        }
        node.find('div.disable input').change(function(){
            self.parent.parent.display['object'].saveActions();
        }).attr('checked',data['disabled']);
        node.find('div.delete').click(function(){
            $(this).parent().remove();
            self.parent.parent.display['object'].saveActions();
        });
        return node;
    },
    updateAction:function(self, form, node){
        if (!node){
            node = self.addAction({});
            if (self.droppos){
                var xat = parseInt(self.droppos[1]/40);
                var ino = $('div.action',self.parent.actions).eq(xat);
                if (ino.length){
                    try{
                        ino.before(node);
                    }catch(e){
                        node.appendTo(self.parent.actions);
                    }
                }else{
                    node.appendTo(self.parent.actions);
                }
            }else{
            }
            self.droppos = null;
        }
        $.data(node[0],'name',self.info.name);
        $.data(node[0],'data',self.getData(form));
        if (['if','and','or','while','elif'].indexOf(self.info.name)===-1){
            node.find('div.text').html(self.text(self.getData(form)),true);
        }
        self.parent.parent.display['object'].saveActions();
        return node;
    },
    showForm:function(self, node, data, oncomplete){
        oncomplete = oncomplete || self.updateAction;
        if (node && !data){
            data = $.data(node[0], 'data');
        }
        if (!data)data = {};
        var form = $('<div class="action-dialog ' + self.info.name + '"><div class="title"></div><div class="contents"></div><div class="buttons"><div class="ok">Ok</div><div class="cancel">Cancel</div></div></div>').appendTo('body');
        if (!self.populateForm(form,data)){
            form.remove();
            if (!node){
                return oncomplete(form);
            }
            return false;
        }
        $('#back').show();
        form.show();
        self.update(form)();
        form.find('.ok').click(function(){
            oncomplete(form, node);
            self.closeForm(form)();
        });
        form.find('.cancel').click(self.closeForm(form));
    },
    update:function(self,form) {
        return function(){
            var height = form[0].offsetHeight;
            form.css('margin-top',-height/2+'px');
        };
    },
    closeForm:function(self,form){
        return function(){
            form.remove();
            $('#back').hide();
        };
    },
    populateForm:function(self, node, data){
        var input_types = {
            'any':['number','direction','random','variable','key','randint','timer','custom'],

            'appliesto':[['select','self','other'],['variable','object']],
            'objecttype':['objecttype',['variable','objecttype']],
            'object':[['variable','object']],

            'timer':['timer',['number',0,10,1],['random',0,10]],

            'bigint':[['number', 0, 100, 1],['variable','int'],['randint',0,100]],
            'medint':[['number', 0, 50, 1],['variable','int'],['randint',0,50]],
            'smallint':[['number', 0, 10, 1],['variable','int'],['randint',0,10]],

            'direction':['direction',['variable','float'],['number',0,360],['random',0,360]],
            'speed':[['number',0,10,.2],'percent',['variable','float'],['random',0,10]],

            'bigfloat':[['number', 0, 100, .5],['variable','float'],['random',0,100]],
            'medfloat':[['number', 0, 50,    .5],['variable','float'],['random',0,50]],
            'smallfloat':[['number', 0, 10, .1],['variable','float'],['random',0,10]],
            'float':[['number', 0, 20, .2],['variable','float'],['random',0,20]],

            'bool':['bool',['variable','bool'],'randbool'],
            'not':['not'],
            'vhboth':[['select','both','vertical','horizontal']],
            'compareop':[['select','==','>','<','>=','<=']],
            'string':['string',['variable','string']],
            'key':['key',['variable','int']],
            'variable':['variable'],
            'conditional':null,
        };
        var contents = $('.contents',node).html('');
        $('.title',node).html(self.info.description);
        $.data($(node)[0],'name',self.name);

        var inputs = {};
        var empty = true;
        for (var name in self.info.inputs) {
            var type = self.info.inputs[name];
            if (type == 'conditional'){
                if (!data[name]){
                    data[name] = {};
                }
                continue;
            }
            if (type=='appliesto' && self.parent.parent.display['object'].events.selected.indexOf('collide')!==0){
                continue;
            }
            empty = false;
            $('<label for="' + name + '">' + name + '</label>').appendTo(contents);
            var div = $('<div class="input"></div>').appendTo(contents);
            var value = data[name];
            if (!value){
                value = null;
            }
            inputs[name] = MultiValuable(self.parent, div, input_types[type], value, self.update(node));
        }
        $.data($(node)[0], 'inputs', inputs);
        return !empty;
    },
    getData:function(self,form){
        var data = {};
        var inputs = $.data(form[0], 'inputs');
        for (name in inputs){
            data[name] = inputs[name].value();
        }
        return data;
    },
});

var PluginManager = Class([], {
    id:'#plugins',
    tid:'#plugin-tabs',
    actions:'#object-actions',
    __init__:function(self, parent, addAction){
        self.parent = parent;
        self.plugins = {};
        self.plugintypes = {};
        self.addAction = addAction || function(){};
        self.action = addAction;
        self.types = [];
        self.onloaded = function(){};

        var types = ['move','conditional','other','control'];
        for (var i=0;i<types.length;i++){
            self.addType(types[i]);
        }

        $('button.ok',self.fid).click(function(){
                var data = self._get_data();
                var res = self._validate_form(data);
                if (res!==true){
                        alert('Item '+res+' is required');
                        return;
                }
                self.action(self.cplugin,data);
                self._close_form();
        });
        $('button.cancel',self.fid).click(self._close_form);

        self.loadPlugins();
    },
    addType:function(self,type){
        self.types.push(type);
        var node = $('<div class="tab">'+humanize(type)+'</div>').appendTo(self.tid).click(function(){
            $('div.tab.selected',self.tid).removeClass('selected');
            $(this).addClass('selected');
            $('.plugin-image',self.id).hide().filter('.'+type).show();
        }).addClass('type-'+type);
        if (self.types.length===1){
            node.addClass('selected');
            self.onloaded = function(){
                $('.plugin-image',self.id).hide().filter('.'+type).show();
            }
        }
    },
    loadPlugins:function(self){
        var True=true,False=false,None=null;
        $(self.id).html('');
        self.parent.ajax.send('', {}, function(object){
            for (var i=0;i<object.length;i++){
                self.loadPlugin(object[i]);
            }
            self.onloaded();
            /**var toload = object.plugins.length;
            for (var i=0;i<object.plugins.length;i++){
                self.parent.ajax.send('', {}, function(x){
                        eval('var plugin=' + x.replace(/'([^']+)'\s*:/g, '$1:')); // remove single quotes from object attrs
                        if (self.types.indexOf(plugin.type)===-1){
                            self.addType(plugin.type);
                        }
                        if (self.plugintypes[plugin.name]){
                            self.plugins[plugin.name] = self.plugintypes[plugin.name](self, plugin);
                        }else{
                            self.plugins[plugin.name] = Plugin(self, plugin);
                        }
                        toload -= 1;
                        if (toload === 0){
                            self.onloaded();
                        }
                },{url:'plugins/'+object.plugins[i]+'/'+object.plugins[i]+'.info', type:'text'});
            }**/
        },{url:'plugins/all.cache'});
    },
    loadPlugin:function(self,plugin){
        var name = plugin[0];
        plugin = plugin[1];
        if (self.types.indexOf(plugin.type)===-1)
            self.addType(plugin.type);
        if (self.plugintypes[plugin.name]){
            self.plugins[plugin.name] = self.plugintypes[plugin.name](self, plugin);
        }else{
            self.plugins[plugin.name] = Plugin(self, plugin);
        }
    },
    icon:function(self,name){
        return self.plugins[name].info.icon;
    }
});

function jQueryPlugin(name, defaults, helpers, init, allforone) {
    $.fn[name] = function (options) {
        if (typeof(options) === 'string') {
            if (typeof(helpers[options]) !== 'undefined') {
                var args = arguments;
                if (allforone) {
                    return helpers[options].apply($.data(this[0], name), Array.prototype.slice.call(args, 1));
                } else {
                    if (this.length>1){
                        return this.each(function () {
                            return helpers[options].apply($.data(this, name), Array.prototype.slice.call(args, 1));
                        });
                    }else{
                        return helpers[options].apply($.data(this[0], name), Array.prototype.slice.call(args, 1));
                    }
                }
            }
        }

        if ($.data(this, name)){
            return; // maybe throw an error == already initialized?
        }

        if (allforone) {
            var widget = {};
            widget.settings = $.extend({}, defaults, options);
            widget.node = $(this); // the individual node
            $.data(widget.node[0], name, widget);
            init.apply(widget, [widget.settings]);
            return this;
        } else {
            return this.each(function () {
                var widget = {};
                widget.settings = $.extend({}, defaults, options);
                widget.node = $(this); // the individual node
                $.data(this, name, widget);

                init.apply(widget, [widget.settings]);
                return this;
            });
        }
    };
}

// actually make the plugin
// *always use degrees* <for now>
jQueryPlugin('direction',
    {
        value:0,
    },
    { // helpers
        value: function(){
            return this.settings.value;
        },
        set: function (value) {
            return this.set(value);
        },
        check: function() {
            return this.check();
        }
    },
    function (settings) { // init
        var that = this;
        this.node.addClass('direction-widget');
        var cardinal = $('<div class="cardinal"></div>').appendTo(this.node);
        var directions = {'bl':135,'b':90,'br':45,'r':0,'tr':315,'t':270,'tl':225,'l':180};
        for (var dir in directions){
            (function(dir, theta){
                $('<div class="'+dir+'"></div>').appendTo(cardinal).click(function(){
                    that.set(theta);
                });
            }(dir,directions[dir]));
        }
        var down = true;
        var cwidth = 84;
        var circle = $('<div class="circle"><div class="handle"></div><div class="number"></div></div>').appendTo(this.node).mousedown(function(e){
            var c = $(this);
            function mm(e){
                var off = c.offset();
                var theta = Math.atan2(e.pageY - (off.top + cwidth/2), e.pageX - (off.left + cwidth/2));
                that.set(parseInt(theta/Math.PI*180));
            }
            function mu(){
                $('body').unbind('mousemove',mm).unbind('mouseup',mu);
            }
            mm(e);
            $('body').bind('mousemove',mm).bind('mouseup',mu);
        });
        that.update = function(){
            $('.cardinal div',that.node).removeClass('selected');
            for (var dir in directions){
                if (directions[dir]==that.settings.value){
                    $('.'+dir,that.node).addClass('selected');
                }
            }
            $('.circle .handle',that.node).css('left',Math.cos(that.settings.value/180*Math.PI)*cwidth/2 + cwidth/2 - 4.5 + 'px')
                .css('top',Math.sin(that.settings.value/180*Math.PI)*cwidth/2 + cwidth/2 - 4.5 + 'px');
            $('.circle .number',that.node).html(that.settings.value);
        }
        that.set = function(val){
            val = parseFloat(val);
            that.settings.value = val;
            that.update();
        };
        that.check = function(){
            return !isNaN(parseFloat(that.settings.value));
        };
        that.update()
    },
    false // allforone
);


