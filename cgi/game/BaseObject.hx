package game;
import game.Game;
import game.Sprite;
import game.Vector;
import flash.geom.Point;
import flash.events.Event;
import flash.display.BitmapData;
import flash.display.Loader;
import flash.net.URLRequest;
import flash.ui.Keyboard;

class BaseObject extends ImageSprite {
  
  
  
  public function moveDirection(direction:Float, speed:Float){
    var v = new Vector(direction, speed);
    this.x += v.x;this.y += v.y;
  }
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
    }catch(e:String){trace(e);}
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
    nv.magnitude = -2;
    var a:Float = MPoint.angle_to(this.x,this.y,object.x,object.y);
    nv.radians = a;
    for (i in 0...10){
      if (!this.collidesWith(object))break;
      this.x+=nv.x;
      this.y+=nv.y;
    }
    a /= Math.PI/2;
    a = Std.int(a) * Math.PI/2;
    //parent.trace(a);
    this._velocity.bounce_off(a+Math.PI/2);
  }
  
  
  public function setOpacity(opacity:Float, opacity_percent:Bool, relative:Bool){
    if (opacity_percent)this.opacity *= opacity;
    else if (relative)this.opacity += opacity;
    else this.opacity = opacity;
  }
  
  
  public function collisionAt(x:Float,y:Float, object:String, relative:Bool){
    var ox:Float;var oy:Float;
    ox = this.x;oy = this.y;
    if (relative){
      this.x+=x;
      this.y+=y;
    }else{
      this.x=x;
      this.y=y;
    }
    for (obj in this.parent.objects.get(cast Type.resolveClass(object)).iterator()){
      if (obj==this)continue;
      if (this.collidesWith(obj)){
        this.x=ox;this.y=oy;
        return true;
      }
    }
    this.x=ox;this.y=oy;
    return false;
  }
  
  
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
  public function gravityTowards(x:Float, y:Float, gravity:Float, relative:Bool){
    var v = Vector.frompos(x-this.x,y-this.y);
    v.magnitude = gravity;
    if (relative)
      this._gravity = this._gravity.add(v);
    else
      this._gravity = v;
  }
  
  public function limitSpeed(speed:Float){
    if (this.speed>speed)this.speed = speed;
    if (this.speed<-speed)this.speed = -speed;
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
