public function moveToCollision(dir:Float, amount:Float, object:String){
  if (0==amount)return;
  var nv = new Vector(dir, amount);
  var amt = 10;
  if (nv.magnitude>10)amt = Std.int(nv.magnitude/2);
  nv.magnitude/=amt*1.0;
  if (this.collisionAt(0,0, object, true)){
    for (i in 0...amt){
//trace(-nv.x + ':' + (-nv.y));
      this.moveTo(-nv.x,-nv.y,true);
      if (!this.collisionAt(0,0, object, true))return;
    }
  }else{
    for (i in 0...amt){
      this.moveTo(nv.x,nv.y,true);
      if (this.collisionAt(0,0, object, true)){
        this.moveTo(-nv.x,-nv.y,true);
        return;
      }
    }
    //this.moveTo(-nv.x*amount,-nv.y*amount,true);
  }
}
