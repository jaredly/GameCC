
// good Jan 5
var LoadingBar = Class([], {
    tid: '#loading',
    pid: '#loading .progressbar',
    __init__: function(self, oncomplete){
        self.loaded = 0;
        self.loading = false;
        self.full = 0;
        self.oncomplete = oncomplete;
        $(self.tid).hide()
        $(self.pid).progressbar({value:0});
    },
    load: function(self, full){
        self.full = full;
        self.loading = true;
        self.loaded = 0;
        $(self.pid).progressbar('option','value',0).show();
    },
    close: function(self) {
        self.loaded = 0;
        self.full = 0;
        self.loading = false;
        $(self.tid).hide();
    },
    increment: function(self){
        if (!self.loading) {
            return;
        }
        self.loaded += 1;
        $(self.pid).progressbar('option', 'value', self.loaded/self.full*100).show();
        if (self.loaded >= self.full) {
            self.oncomplete();
        }
    },
});
// redoing Jan 5
/**
 * umm
 */
var AjaxMuffin = Class([], {
    __init__: function(self, parent){
        self.parent = parent;
        self._queue = [];
        self._queueing = false;
    },
    queue: function(self, command, data, oncomplete, options) {
        data['cmd'] = command;
        if (typeof(options) === 'undefined')options = {};
        if (typeof(options['url']) === 'undefined')
            options['url'] = 'cgi/index.py';
        data['pid'] = self.parent.project.pid;
        options['data'] = data;
        options['oncomplete'] = oncomplete;
        self._send_queued(options);
    },
    send: function(self, command, data, oncomplete, options) {
        data['cmd'] = command;
        if (typeof(options) === 'undefined')options = {};
        if (typeof(options['url']) === 'undefined')
            options['url'] = 'cgi/index.py';
        if (self.parent && self.parent.project && typeof(data['pid'])=='undefined' && self.parent.project.pid)
            data['pid'] = self.parent.project.pid;
        options['data'] = data;
        options['oncomplete'] = oncomplete || function(){};
        if (typeof(options['onerror']) === 'undefined') {
            options['onerror'] = function(error){
                self.parent.errors.log(error);
            };
        }
        self._send(options);
    },
    send_queued: function(self) {
        alert('dont use send_queued.');
    },
    _send_queued: function(self, options) {
        self._queue.push(options);
        if (!self._queueing) { // || self._queue.length == 1
            self._queueing = true;
            self._advance_queue();
        }
    },
    _advance_queue: function(self) {
        if (!self._queueing)return;
        if (!self._queue.length){
            self._queueing = false;
            return;
        }
        var options = self._queue.shift();
        var _old_oncomplete = options['oncomplete'] || function(){};
        var _old_onerror = options['onerror'] || function(){};
        var oncomplete = function(){
            self._advance_queue();
            _old_oncomplete.apply(null,arguments);
        };
        var onerror = function(){
            self._advance_queue();
            _old_onerror(null,arguments);
        };
        options['oncomplete'] = oncomplete;
        options['onerror'] = onerror;
        self._send(options);
    },
    _send: function(self, options) {
        $('#loading-small').show();
        if (!options['oncomplete'])
            debugger;
        $.ajax({
            async:true,
            cache:false,
            data:options['data'],
            dataType:'text',
            error:options['onerror'],
            success:function(result){
                $('#loading-small').hide();
                if (!options.type || options.type == 'json'){
                    if (!result){
                        alert('missing '+url);
                        return options['onerror']('url');
                    }
                    try {
                        var False = false,True=true,None=null;
                        eval('var object = '+result);
                    } catch(e) {
                        return options['onerror']('json');
                    }
                    if (object.error){
                        return options['onerror']('server');
                    }
                    options['oncomplete'](object);
                } else {
                    options['oncomplete'](result);
                }
            },
            type:'POST',
            url:options['url']
        });
    },
});

/**
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
**/
