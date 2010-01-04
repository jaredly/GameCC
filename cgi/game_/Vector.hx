package game;

class Vector {
  public var radians:Float;
  public var magnitude:Float;
  public inline function _get_degrees(){return this.radians / Math.PI * 180;}
  public inline function _set_degrees(x:Float){this.radians = x * Math.PI / 180;return x;}
  public var degrees(_get_degrees,_set_degrees):Float;
  public inline function _get_x(){return Math.cos(this.radians)*this.magnitude;}
  public inline function _set_x(x:Float){
    var y = this.y;
    this.radians = Math.atan2(y,x);
    this.magnitude = Math.sqrt(x*x+y*y);
    return x;
  }
  public inline function _get_y(){return Math.sin(this.radians)*this.magnitude;}
  public inline function _set_y(y:Float){
    var x = this.x;
    this.radians = Math.atan2(y,x);
    this.magnitude = Math.sqrt(x*x+y*y);
    return y;
  }
  public var x(_get_x,_set_x):Float;
  public var y(_get_y,_set_y):Float;
  
  public function new(degrees:Float, magnitude:Float) {
    this.degrees = degrees;
    this.magnitude = magnitude;
  }
  public static function frompos(x:Float,y:Float){
    return new Vector(Math.atan2(y,x),Math.sqrt(x*x+y*y));
  }
  public function add(v:Vector){
    return Vector.frompos(this.x + v.x, this.y+v.y);
  }
  
  public function bounce_off(angle:Float){
  	this.radians = angle*2 - this.radians;
  	return this;
  }
  public function part(angle:Float){
    return new Vector(angle, Math.cos(angle*Math.PI/180-this.radians)*this.magnitude);
  }
  public function clone(){
    return new Vector(this.degrees,this.magnitude);
  }
  public function reverse(){
    return new Vector(this.degrees + 180,this.magnitude);
  }
  public function set(v:Vector, relative:Bool){
    if (relative){
      v = v.add(this);
    }
    this.radians = v.radians;
    this.magnitude = v.magnitude;
  }
}

class Color {
    public static function rgb( r : Int, g : Int, b : Int ) : Int {
        return (r << 16) | (g << 8) | b;
    }
}

class Random {
    public static function randrange(start:Int,?end:Int):Int{
        if (end==null){
            end=start;
            start=0;
        }
        return Std.int(Math.random()*(end-start) + start);
    }
    public static function random(){
        return Math.random();
    }
}
