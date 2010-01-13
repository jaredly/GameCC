public function bounceAgainst(object:BaseObject){
  var nv:Vector = new Vector(0,0);
  nv.magnitude = -2;
  var a:Float = MPoint.angle_to(this.x,this.y,object.x,object.y);
  nv.radians = a;
  for (i in 0...10){
    if (!this.collidesWith(object))break;
    this.x+=nv.x;
    this.y+=nv.y;
  }
  a /= Math.PI/2;
  a = Std.int(a) * Math.PI/2;
  //parent.trace(a);
  this._velocity.bounce_off(a+Math.PI/2);
}
