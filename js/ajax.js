
var AjaxMuffin = Class([], {
    __init__: function(self, parent){
        self.parent = parent;
        self.queue = [];
        self.loading = false;
        self.queuing = false;
        self.fullload = 0;
        self.stopped = false;
        self.onstopped = function(){};
        $('#loading .progressbar').progressbar({value:0});
    },

    setloadbar: function(self, num, func){
        self.loading = num;
        self.fullload = num;
        self.onstopped = func || function(){};
    },

    send: function(self, command, data, func, options){
        options = options || {};
        func = func || function(){};
        data['cmd'] = command;
        if (!data['project'] && self.parent.project && self.parent.project.info.name){
            data['project'] = self.parent.project.info.name;
        }
        var url = options.url || 'cgi/index.py';
        if (!self.loading){
            self.loading = true;
            $('#loading-small').show();
        }
        if (options.showstop){
            self.stopped = true;
            self.showStop();
        }
        $('#loading-small').show();
        $.post(url, data, function(result){
            $('#loading-small').hide();
            if (!self.stopped){
                self.stopload();
            } else if (options.increment) {
                self.increment(options.increment);
            }
            if (!options.type || options.type == 'json'){
                if (!result){
                    alert('missing '+url);
                    if (options.queued)
                        self.advance_queue();
                    return;
                }
                try {
                    var False = false,True=true,None=null;
                    eval('var object = '+result);
                } catch(e) {
                    alert('AJAX Exception: '+result);
                    if (options.queued)
                        self.advance_queue();
                    return
                }
                if (object.error){
                    alert('Python exception: ' + object.error);
                    return;
                }
                func.apply(self, [object]);
            } else {
                func.apply(self, [result]);
            }
            if (options.queued)
                self.advance_queue();
            return
        });
    },

    increment: function(self, i){
        i = i || 1;
        self.loading -= i;
        $('#loading .progressbar').progressbar('value',100 * (self.fullload - self.loading) / self.fullload);
        if (!self.loading){
            self.unStop();
        }
    },

    stopload:function(self){
        $('#loading-small').hide();
        self.loading = false;
    },

    showStop: function(self){
        $('#back, #loading').show();
        $('#loading .progressbar').progressbar('value',0);
    },

    unStop: function(self){
        $('#back, #loading, #loading-small').hide();
        $('#loading .progressbar').progressbar('value',0);
        self.queue = [];
        self.onstopped();
    },

    advance_queue: function(self){
        if (self.queue.length){
            self.queue.shift();
            if (self.queue.length){
                self.send.apply(self,self.queue[0]);
            } else {
                self.queuing = false;
                $('#loading-small').hide();
            }
        }
    },

    start_queue: function(self){
        if (self.queuing)return;
        self.send.apply(self, self.queue[0]);
        self.queuing = true;
    },

    send_queued: function(self, command, data, func, options){
        if (!options)options = {};
        options.queued = true;
        var start = false;;
        if (!self.queue.length)start = true;
        self.queue.push([command, data, func, options]);
        if (start){
            self.start_queue();
        }
    },
});
