package game;

import game.BaseObject;

class Group {
  public var baseobj:Class<BaseObject>;
  public var _classes:Array<Class<BaseObject>>;
  public var _items:Array<Array<BaseObject>>;
  
  public function new(){
    this._classes = [];
    this._classes.push(cast Type.resolveClass('BaseObject'));
    this._items = [[]];
  }
  public function append(obj:BaseObject) {
    /* WARNING: does not check redundant....
    if (obj in this._classes[0]){
      raise Exception,'object already in group';
    }*/
    var cls:Class<BaseObject> = Type.getClass(obj);
    while (cls != null) {
      var flag = true;
      for (i in 0...this._classes.length){
        if (this._classes[i] == cls) {
          this._items[i].push(obj);
          flag = false;
          break;
        }
      }
      if (flag) {
        this._classes.push(cls);
        this._items.push([obj]);
      }
      if (cls == Type.resolveClass('BaseObject'))break;
      cls = cast Type.getSuperClass(cls);
    }
    obj.create();
  }
  public function remove(obj:BaseObject){
    var cls:Class<Dynamic> = Type.getClass(obj);
    while (cls != null) {
      for (i in 0...this._classes.length){
        if (this._classes[i] == cls) {
          this._items[i].remove(obj);
          break;
        }
      }
      cls = Type.getSuperClass(cls);
    }
    obj.destroy();
  }
  public function get(cls:Class<BaseObject>){
    for (i in 0...this._classes.length){
      if (this._classes[i] == cls) {
        return this._items[i];
      }
    }
    return [];
  }
  public function iterator(){
    return this.get(BaseObject).iterator();
  }
}
