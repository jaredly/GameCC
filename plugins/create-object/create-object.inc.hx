public function createObject(object:String, x:Float, y:Float, relative:Bool, direction:Float, speed:Float){
  try{
  if (relative){
    x+=this.x;
    y+=this.y;
  }
  var obj:BaseObject = Type.createInstance(this.parent.objectdict.get(object),[this.parent,x,y]);
  obj.setV(direction, speed,false);
  this.parent.add(obj);
  obj.created();
  }catch(e:String){trace(e);}
}
