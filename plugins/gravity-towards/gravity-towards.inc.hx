public function gravityTowards(x:Float, y:Float, gravity:Float, relative:Bool){
  var v = Vector.frompos(x-this.x,y-this.y);
  v.magnitude = gravity;
  if (relative)
    this._gravity = this._gravity.add(v);
  else
    this._gravity = v;
}
