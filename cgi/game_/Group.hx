package game;

import game.ObjectBase;

class Group {
  public var baseobj:Class<ObjectBase>;
  public var _classes:Array<Class<Dynamic>>;
  public var _items:Array<Array<ObjectBase>>;
  
  public function new(baseobj:Class<ObjectBase>){
    this.baseobj = baseobj;
    this._classes = [baseobj];
    this._items = [[]];
  }
  public function append(obj:ObjectBase) {
    /* WARNING: does not check redundant....
    if (obj in this._classes[0]){
      raise Exception,'object already in group';
    }*/
    var cls:Class<Dynamic> = Type.getClass(obj);
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
      cls = Type.getSuperClass(cls);
    }
    obj.create();
  }
  public function remove(obj:ObjectBase){
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
  public function get(cls:Class<ObjectBase>){
    for (i in 0...this._classes.length){
      if (this._classes[i] == cls) {
        return this._items[i];
      }
    }
    return [];
  }
  public function iterator(){
    return this.get(this.baseobj).iterator();
  }
}
