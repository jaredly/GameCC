package game;
import game.Game;
import game.ObjectBase;
import game.Vector;
import flash.geom.Point;
import flash.events.Event;
import flash.display.BitmapData;
import flash.display.Loader;
import flash.net.URLRequest;
import flash.ui.Keyboard;

class BaseObject extends ObjectBase {
  
  
  
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
  
  public function setTimer(timer:Int, amount:Int, relative:Bool){
    if (relative)this.timers[timer] += amount;
    else this.timers[timer] = amount;
  }
  public function setDirection(direction:Float, relative:Bool){
    if (relative) this.direction += direction;
    else this.direction = direction;
  }
  
  public function createObject(object:String, x:Float, y:Float, relative:Bool, direction:Float, speed:Float){
    try{
    if (relative){
      x+=this.x;
      y+=this.y;
    }
    var obj:BaseObject = Type.createInstance(this.parent.objectdict.get(object),[this.parent,x,y]);
    obj.setV(direction, speed,false);
    this.parent.add(obj);
    obj.created();
    }catch(e:String){this.parent.log=e;}
  }
  
  
  
  public function setGravity(direction:Float, speed:Float){
    this._gravity = new Vector(direction, speed);
  }
  
  public function setHspeed(speed:Float, speed_percent:Bool, relative:Bool){
    if (speed_percent)
      this.hspeed *= speed;
    else if (relative)
      this.hspeed += speed;
    else
      this.hspeed = speed;
  }
  
  public function setSpeed(speed:Float, speed_percent:Bool, relative:Bool){
    if (speed_percent) this.speed *= speed;
    else if (relative) this.speed += speed;
    else this.speed = speed; 
  }
  public function bounceAgainst(object:BaseObject){
    var nv:Vector = new Vector(0,0);
    nv.m = -2;
    var a:Float = MPoint.angle_to(this.pos,object.pos);
    nv.t = a;
    for (i in 0...10){
      if (!this.collidesWith(object))break;
      this.pos.x+=nv.x();
      this.pos.y+=nv.y();
    }
    a /= Math.PI/2;
    a = Std.int(a) * Math.PI/2;
    parent.log += ''+a+'
  ';
    this.v.bounce_off(a+Math.PI/2);
  }
  
  
  public function setOpacity(opacity:Float, opacity_percent:Bool, relative:Bool){
    if (opacity_percent)this.opacity *= opacity;
    else if (relative)this.opacity += opacity;
    else this.opacity = opacity;
  }
  
  public function collisionAt(pos:Point, object:String){
    this.x+=pos.x;
    this.y+=pos.y;
    for (obj in this.parent.objects.get(object).iterator()){
      if (obj==this)continue;
      if (this.collidesWith(obj)){
        this.x-=pos.x;this.y-=pos.y;
        return true;
      }
    }
    this.x-=pos.x;this.y-=pos.y;
    return false;
  }
  
  
  public function moveToCollision(dir:Float, amount:Float, object:String){
    var nv = new Vector(dir, amount);
    nv.m/=amount;
    if (this.collisionAt(0,0, object)){
      for (i in 0...Std.int(amount)){
        this.moveTo(-nv.x(),-nv.y(),true);
        if (!this.collisionAt(new Point(0,0), object))return;
      }
    }else{
      for (i in 0...Std.int(amount)){
        this.moveTo(nv.x(),nv.y(),true);
        if (this.collisionAt(0,0, object)){
          this.moveTo(-nv.x(),-nv.y(),true);
          return;
        }
      }
      this.moveTo(-nv.x()*amount,-nv.y()*amount,true);this._update();
    }
  }
  
  public function setVspeed(speed:Float, speed_percent:Bool, relative:Bool){
    if (speed_percent){this.vspeed *= speed;}
    else if (relative){this.vspeed += speed;}
    else{this.vspeed = speed;}
  }
  public function keepOnScreen(bounce:Bool){
    limitPos(0,0,this.parent.size[0],this.parent.size[1],0,bounce);
  }
  
  public function setV(direction:Float, speed:Float, rel:Bool){
    if (rel){
      this._velocity = this._velocity.add(new Vector(direction,speed));
    }else{
      this._velocity = new Vector(direction, speed);
    }
  }
  public function setImageRotation(rotation:Float, relative:Bool){
    if (relative)this.rotation += rotation;
    else this.rotation = rotation;
  }
  
  public function moveTo(x:Float, y:Float, relative:Bool){
    if (relative){
      this.x+=x;
      this.y+=y;
    }else{
      this.x=x;
      this.y=y;
    }
  }
  
  

}
