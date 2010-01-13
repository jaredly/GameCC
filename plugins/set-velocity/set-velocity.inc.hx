public function setV(direction:Float, speed:Float, rel:Bool){
  if (rel){
    this._velocity = this._velocity.add(new Vector(direction,speed));
  }else{
    this._velocity = new Vector(direction, speed);
  }
}
