public function moveTo(x:Float, y:Float, relative:Bool){
  if (relative){
    this.x+=x;
    this.y+=y;
  }else{
    this.x=x;
    this.y=y;
  }
}
