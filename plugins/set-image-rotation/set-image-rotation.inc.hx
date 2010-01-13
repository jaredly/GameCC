public function setImageRotation(rotation:Float, relative:Bool){
  if (relative)this.rotation += rotation;
  else this.rotation = rotation;
}
