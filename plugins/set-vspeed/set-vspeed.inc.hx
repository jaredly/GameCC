public function setVspeed(speed:Float, speed_percent:Bool, relative:Bool){
  if (speed_percent){this.vspeed *= speed;}
  else if (relative){this.vspeed += speed;}
  else{this.vspeed = speed;}
}
