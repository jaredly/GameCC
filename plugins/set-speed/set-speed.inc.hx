public function setSpeed(speed:Float, speed_percent:Bool, relative:Bool){
  if (speed_percent) this.speed *= speed;
  else if (relative) this.speed += speed;
  else this.speed = speed; 
} 