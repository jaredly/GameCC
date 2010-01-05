
/**
    get plugins
        list_plugins -> handled by "PluginManager"
        async -- load each plugin. show loading bar
    list projects
        dialog box: open or new
        handled by "OpenDialog"
    to load a project:
        load_project -> {metadata, images, objects, maps, rawimages}
            handled by "Project" object


**/

var NameDialog = Class([], {
    id:'#name-dialog',
    __init__:function (self) {
        self.callback = function(){};
        $(self.id).dialog({
            bgiframe: true,
            autoOpen: false,
            modal: true,
            buttons: {
                Ok: self.onok,
                Cancel: function() {
                    $(this).dialog('close');
                }
            },
            close: function() {
                $('.i-name',self.id).val('').removeClass('ui-state-error');
            }
        });
        $('.i-name', self.id).keydown(function(e){
            if (e.keyCode == 13){
                self.onok();
                return killE(e);
            }
        });
    },
    onok:function(self) {
        if (!$('.i-name', self.id).val()){
            $('.i-name', self.id).addClass('ui-state-error');
        } else {
            var name = $('.i-name',self.id).val();
            $(this).dialog('close');
            self.callback(name);
        }
    },
    open:function(self, callback) {
        self.callback = callback;
        $(self.id).dialog('open');
        $('.i-name', self.id).focus();
    }
});


/**
    Tab Manager class:
        __init__(onchange:function, rightclick:function)
        add(type:(image|object|map), name:string, switchto:bool)
        remove(type:string, name:string)
        change(type:string, from:string, to:string)
        preview(type:string,from:string,to:string)
        clear(type:string)
**/
var TabMan = Class([], {
    id:'#sidebar',
    __init__: function(self, parent, onchange, rightclick){
        self.parent = parent;
        self.tabs = {};
        self.onchange = onchange || function(){};
        self.rightclick = rightclick || function(){};
        self.selected = null;
    },
    add: function(self, type, name, switchto){
        if (!self.tabs[type]){
            self.tabs[type] = {};
            $('#' + type + '-list').sortable({
                placeholder: 'ui-state-highlight',
                axis:'y',
                distance:10,
                stop:function(e,ui){
                    var names = [];
                    var parent = ui.item.parent();
                    var type = parent[0].id.split('-')[0] + 's';
                    parent.find('.handle').each(function(){
                        names.push(this.innerHTML);
                    });
                    self.parent.project.save_order(type,names);
                }
            });
        }
        self.tabs[type][name] = $('<div class="handle">' + name + '</div>').appendTo('#' + type + '-list').click(function(e){
            var name = $(this).html();
            self.onchange(self.selected, [type, name]);
            self.selected = [type, name];
            $('div.handle', self.id).removeClass('selected');
            $(this).addClass('selected');
        }).bind('contextmenu',function(e){
            self.rightclick(e, type, $(this).html());
            return killE(e);
        });
        if (switchto)
            self.tabs[type][name].click();
    },
    remove: function(self, type, name){
        $(self.tabs[type][name]).remove();
        delete self.tabs[type][name];
    },
    change: function(self, type, from, to){
        self.tabs[type][from].html(to);
        self.tabs[type][to] = self.tabs[type][from];
        delete self.tabs[type][from];
    },
    preview: function(self, type, from, to) {
        self.tabs[type][from].html(to);
    },
    clear: function(self, type){
        $('#' + type + '-list').html('');
    }
});

/**
    Editor: main gamecc editor class
**/
var Editor = Class([], {
    /*good*/
    __init__: function(self){
        self._small = true;
        self.ajax = AjaxMuffin(self);
        self.imagescale = ImageScale(self);
        self.imagepicker = ImagePicker(self);
        self.media = MediaLibrary(self);
        self.tabs = TabMan(self, self.onTabChange, self.onRightClick);
        self.plugins = PluginManager(self);
        self.namedialog = NameDialog();
        self.project = Project(self, {
            'load':self._onload,
            'delete':self.clear,
            'loadAsset':self.loadAsset,
        });
        self.project_dialog = ProjectDialog(self, {
            'open':self.onopen,
            'new':self.onnew,
            'remove':self.onremove
        });
        self.display = {};
        self.display['image']    = DisplayImage(self);
        self.display['object'] = DisplayObject(self);
        self.display['map']        = DisplayMap(self);
        if (document.location.hash){
            self.project.open(document.location.hash.slice(1));
        }else{
            self.project_dialog.open();
        }
    },
    /*good*/
    loadAsset: function(self, type, name){
        self.tabs.add(type, name, !self.project.loading);
        if (!self.project.loading) {
            self.display[type].selectname();
        }
    },
    /*good*/
    onTabChange: function(self, from, to){
        if (from){
            self.display[from[0]].unload();
        }
        self.display[to[0]].load(to[1]);
    },
    /*good -- right click callback for asset sidebar*/
    onRightClick: function(self, event, type, name){
        contextMenu([['Delete',self.removeAsset(type, name)],
            ['Clone', self.cloneAsset(type, name)]])(event);
    },
    /*good*/
    removeAsset: function(self, type, name){
        return function(){
            if (self.display[type].object === self.project.data[type][name]){
                self.display[type].unload();
            }
            self.project.remove(type, name);
            self.tabs.remove(type, name);
        };
    },
    /*good*/
    cloneAsset: function(self, type, name){
        return function(){
            self.project.clone(type, name);
        };
    },
    /*good*/
    onopen: function(self, name){
        self.clear();
        self.project.open(name);
    },
    /*good*/
    onnew: function(self, name){
        self.clear();
        self.namedialog.open(self.project.new);
    },
    /*good*/
    onremove: function(self, name){
        self.project.remove(name);
    },
    /*good*/
    clear: function(self){
        self.tabs.clear('image');
        self.tabs.clear('object');
        self.tabs.clear('map');
        self.display['image'].unload();
        self.display['object'].unload();
        self.display['map'].unload();
    },
    /*good*/
    imgurl: function(self, name){
        if (!name){
            return 'images/noimg.png';
        }
        return 'raw_images/' + name;
    },
    objImage: function(self, name){
        var obj = self.project.data['object'][name];
        if (!obj.info.image || !self.project.data['image'][obj.info.image]
                || !self.imgurl(self.project.data['image'][obj.info.image].info.subimages.length)){
            return self.imgurl(null);
        }
        return self.imgurl(self.project.data['image'][obj.info.image].info.subimages[0]);
    },
    objScaled: function(self, name, size) {
        var iname = self.project.data['object'][name].info.image;
        if (!iname || !self.project.data['image'][iname]
                || !self.imgurl(self.project.data['image'][iname].info.subimages.length)){
            return self.imagescale.get_scaled(null, size);
        }
        return self.imagescale.get_scaled(self.project.data['image'][iname].info.subimages[0], size);
    },
    /** TODO change name... and add killpreview **/
    preview: function(self) {
        self.ajax.send('project/preview',{},function(res){
            openIframe('preview/'+res.name+'.html',function(){},res.width,res.height);
        });
    }
});


var gcc;
$(function(){
    gcc = Editor();
});
