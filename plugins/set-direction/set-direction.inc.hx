public function setDirection(direction:Float, relative:Bool){
  if (relative) this.direction += direction;
  else this.direction = direction;
}
