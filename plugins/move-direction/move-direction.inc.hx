public function moveDirection(direction:Float, speed:Float){
  var v = new Vector(direction, speed);
  this.x += v.x;this.y += v.y;
}
