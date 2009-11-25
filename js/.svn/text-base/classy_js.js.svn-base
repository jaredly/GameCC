var range = function(x){for (var a=[],b=0;b<x;b++){a.push(b);};return a};
var to_array = function(a){return Array.prototype.slice.call(a,0);};

function new_class(){
    var meta = function(cls,self,func){
        self[func] = function(){
            var args = [self].concat(to_array(arguments));
            /**if (cls[func].length > args.length)
                throw new Exception("Wrong number of arguments: "+args);**/
            return cls[func].apply(this,args);
        }
    }
    var _extends = to_array(arguments);
    
    var cls = function(){
        var self = {};self.__init__ = function(){};
        self._class = cls;
        var args = to_array(arguments);
        
        /**for each(ext in extends){
            for (attr in ext){
                if (typeof(ext[attr])!="function"){
                    self[attr] = ext[attr];
                }else{
                    meta(ext,self,attr);
                }
            }
        }**/
        for (attr in cls){
            if (typeof(cls[attr])!="function"){
                self[attr] = cls[attr];
            }else{
                meta(cls,self,attr);
            }
        }
        self.__init__.apply(self,args);
        return self;
    }
    
    for (var i=0;i<_extends.length;i++){
        var ext = _extends[i];
        for (attr in ext){
            if (attr=='prototype')continue;
            cls[attr] = ext[attr];
        }
    }
    
    //cls._class_name = name;
    //cls.__init__ = function(){};
    return cls
}

function Class(inherits,def){
    var that = new_class.apply(null,inherits || []);
    for (i in def){
        that[i] = def[i];
    }
    return that;
}
