public function moveTowards(x:Float, y:Float, amount:Float, amount_percent:Bool, relative:Bool){
  if (relative){x+=this.x;y+=this.y;}
  var nv = Vector.frompos(x-this.x,y-this.y);
  if (amount_percent){
    nv.magnitude *= amount;
  }else{
    nv.magnitude = amount;
  }
  this.x+=nv.x;
  this.y+=nv.y;
}
