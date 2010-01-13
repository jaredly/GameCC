public function limitSpeed(speed:Float){
  if (this.speed>speed)this.speed = speed;
  if (this.speed<-speed)this.speed = -speed;
}
