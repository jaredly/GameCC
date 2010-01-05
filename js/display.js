
var Display = Class([], {
    tid:null,
    object:null,
    __init__:function (self, parent) {
        self.parent = parent;
        $('.name input',self.tid).blur(function(){
            var res = self.object.set_name(this.value);
            this.value = res;
        }).keyup(function(){
            self.object.preview_name(this.value);
        }).keydown(function(e){
            if (e.keyCode == 13){
                $(this).blur();
            }
        });
        self.setup();
    },
    setup:function (self) {
    },
    load:function (self, name) {
        self.object = self.parent.project.data[self.type][name];
        $(self.tid).show();
        $('.name input',self.tid).val(name).focus().select();
        return true;
    },
    selectname:function(self) {
        $('.name input',self.tid).focus().select();
    },
    // zero stuff out, etc.
    unload:function (self) {
        self.object = null;
        $(self.tid).hide();
        return true;
    },
    tab:function (self) {
        return $(self.tid);
    },
});
