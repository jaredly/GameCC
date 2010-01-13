public function collisionAt(x:Float,y:Float, object:String, relative:Bool){
  var ox:Float;var oy:Float;
  ox = this.x;oy = this.y;
  if (relative){
    this.x+=x;
    this.y+=y;
  }else{
    this.x=x;
    this.y=y;
  }
  for (obj in this.parent.objects.get(cast Type.resolveClass(object)).iterator()){
    if (obj==this)continue;
    if (this.collidesWith(obj)){
      this.x=ox;this.y=oy;
      return true;
    }
  }
  this.x=ox;this.y=oy;
  return false;
}
