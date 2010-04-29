public function setHspeed(speed:Float, speed_percent:Bool, relative:Bool){
  if (speed_percent)
    this.hspeed *= speed;
  else if (relative)
    this.hspeed += speed;
  else
    this.hspeed = speed;
}
