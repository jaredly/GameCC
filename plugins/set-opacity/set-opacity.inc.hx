public function setOpacity(opacity:Float, opacity_percent:Bool, relative:Bool){
  if (opacity_percent)this.opacity *= opacity;
  else if (relative)this.opacity += opacity;
  else this.opacity = opacity;
}
