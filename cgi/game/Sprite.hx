package game;
import flash.geom.Point;
import flash.geom.Rectangle;
import flash.geom.Matrix;
import flash.events.Event;
import flash.events.DataEvent;
import flash.events.AsyncErrorEvent;
import flash.display.BitmapData;
import flash.display.Bitmap;
import flash.display.Loader;
import flash.net.URLRequest;
import flash.ui.Keyboard;
import flash.Error;
import game.Vector;
import game.Game;

class MPoint {
  
  public static function angle_to(x:Float,y:Float,a:Float,b:Float){
    return Math.atan2(b-y,a-x);
  }

}

class ImageSprite {
  public static var imageCache : Hash<BitmapData>;
  public var collisions : Array<String>;
  
  public inline function _get_vspeed(){return this._velocity.y;}
  public inline function _set_vspeed(y:Float){this._velocity._set_y(y);return y;}
  public inline function _get_hspeed(){return this._velocity.x;}
  public inline function _set_hspeed(x:Float){this._velocity._set_x(x);return x;}
  //public inline function _get_x(){return this._x;}
  //public inline function _set_x(x:Float){this._x = x;return x;}
  //public inline function _get_y(){return this._y;}
  //public inline function _set_y(y:Float){this._y = y;return y;}
  public inline function _get_direction(){return this._velocity.degrees;}
  public inline function _set_direction(x){this._velocity.degrees = x;return x;}
  public inline function _get_speed(){return this._velocity.magnitude;}
  public inline function _set_speed(x:Float){this._velocity.magnitude = x; return x;}
  public inline function _get_gdirection(){return this._gravity.degrees;}
  public inline function _set_gdirection(x:Float){this._gravity.degrees = x;return x;}
  public inline function _get_gspeed(){return this._gravity.magnitude;}
  public inline function _set_gspeed(x:Float){this._gravity.magnitude = x;return x;}
  public inline function _get_opacity(){return this._opacity;}
  public inline function _set_opacity(x:Float){this._opacity = x;return x;}
  public inline function _get_rotation(){return this._rotation;}
  public inline function _set_rotation(x:Float){this._rotation = x;return x;}
  
  public var vspeed(_get_vspeed,_set_vspeed):Float;
  public var hspeed(_get_hspeed,_set_hspeed):Float;
  //public var x(_get_x,_set_x):Float;
  //public var y(_get_y,_set_y):Float;
  public var direction(_get_direction,_set_direction):Float;
  public var speed(_get_speed,_set_speed):Float;
  public var gdirection(_get_gdirection,_set_gdirection):Float;
  public var gspeed(_get_gspeed,_set_gspeed):Float;
  public var opacity(_get_opacity,_set_opacity):Float;
  public var rotation(_get_rotation,_set_rotation):Float;
  
  public var _sprite : flash.display.Sprite;
  
  public var image:String;
  public var _velocity:Vector;
  public var _gravity:Vector;
  public var x:Float;
  public var y:Float;
  public var _opacity:Float;
  public var _rotation:Float;
  public var _image:Image;
  public var parent:Game;
  public var timers:Array<Int>;
  public var imagepos:Float;
  public var imagespeed:Float;
  public var height : Int;
  public var width : Int;
  
  public var bm : Bitmap;
  
  public static function loadImage(image:String, oncomplete:Void->Void, debug:Int){
    if (debug>3)trace('loading image '+image);
    var loader : Loader = new Loader();
    loader.contentLoaderInfo.addEventListener(Event.COMPLETE,function(_){
        if (debug>3)trace('loaded image '+image);
        ImageSprite.imageCache.set(image,untyped loader.content.bitmapData);
        oncomplete();
    });
    loader.load(new URLRequest('../raw_images/'+image));
  }
  
  public function new(parent:Game,x:Float,y:Float){
    this.parent = parent;
    if (this.image!="") {
      this._image = parent.images.get(this.image);
    
      this.setup_image();
      this.imagespeed = this._image.speed;
    } else {
      this.imagespeed = 0;
    }
    this.timers = [0,0,0,0,0,0,0,0,0,0];
    this.imagepos = 0;
    if (parent.debug>3)trace('initing obj at '+x+','+y);
    this.x = x;
    this.y = y;
    this._update();
    this._velocity = new Vector(0,0);
    this._gravity = new Vector(0,0);
    
    this._rotation = 0;
    this._opacity = 1.0;
    if (parent.debug>3)trace('inited obj at '+this.x+','+this.y);
  }
  
  function setup_image() {
    this._sprite = new flash.display.Sprite();
    parent.addChild(this._sprite);
    this.bm = new Bitmap(ImageSprite.imageCache.get(this._image.subimages[0]));
    this.bm.x = -ImageSprite.imageCache.get(this._image.subimages[0]).width/2;
    this.bm.y = -ImageSprite.imageCache.get(this._image.subimages[0]).height/2;
    this._sprite.addChild(this.bm);
  }
  
  public function render(screen:BitmapData) {
    this._update();
  }
  
  public function _step() {
  	this._velocity = this._velocity.add(this._gravity);
  	this.move();
    this.imagepos += this.imagespeed;
    if (this.imagepos>=this._image.subimages.length){
      this.imagepos = 0;
    }
    this._update_timers();
    this._check_keydown();
  	if (!this.collideRect(0,0,this.parent.size[0],this.parent.size[1])){
  	  this.off_of_map();
  	}
  	this.step();
  }
  
  public function move() {
  	this.x += this._velocity.x;
  	this.y += this._velocity.y;
  }
  
  public function collideRect(x:Float,y:Float,w:Float,h:Float){
    if (x<this.x && this.x<x+w && y<this.y && this.y<y+h){
      return true;
    }else{
      return false;
    }
  }
  
  public function _check_keydown() {
  	if (parent.keys[48]){key_down_0();}if (parent.keys[49]){key_down_1();}if (parent.keys[50]){key_down_2();}if (parent.keys[51]){key_down_3();}if (parent.keys[52]){key_down_4();}if (parent.keys[53]){key_down_5();}if (parent.keys[54]){key_down_6();}if (parent.keys[55]){key_down_7();}if (parent.keys[56]){key_down_8();}if (parent.keys[57]){key_down_9();}if (parent.keys[65]){key_down_a();}if (parent.keys[66]){key_down_b();}if (parent.keys[67]){key_down_c();}if (parent.keys[68]){key_down_d();}if (parent.keys[69]){key_down_e();}if (parent.keys[70]){key_down_f();}if (parent.keys[71]){key_down_g();}if (parent.keys[72]){key_down_h();}if (parent.keys[73]){key_down_i();}if (parent.keys[74]){key_down_j();}if (parent.keys[75]){key_down_k();}if (parent.keys[76]){key_down_l();}if (parent.keys[77]){key_down_m();}if (parent.keys[78]){key_down_n();}if (parent.keys[79]){key_down_o();}if (parent.keys[80]){key_down_p();}if (parent.keys[81]){key_down_q();}if (parent.keys[82]){key_down_r();}if (parent.keys[83]){key_down_s();}if (parent.keys[84]){key_down_t();}if (parent.keys[85]){key_down_u();}if (parent.keys[86]){key_down_v();}if (parent.keys[87]){key_down_w();}if (parent.keys[88]){key_down_x();}if (parent.keys[89]){key_down_y();}if (parent.keys[90]){key_down_z();}if (parent.keys[96]){key_down_numpad_0();}if (parent.keys[97]){key_down_numpad_1();}if (parent.keys[98]){key_down_numpad_2();}if (parent.keys[99]){key_down_numpad_3();}if (parent.keys[100]){key_down_numpad_4();}if (parent.keys[101]){key_down_numpad_5();}if (parent.keys[102]){key_down_numpad_6();}if (parent.keys[103]){key_down_numpad_7();}if (parent.keys[104]){key_down_numpad_8();}if (parent.keys[105]){key_down_numpad_9();}if (parent.keys[106]){key_down_multiply();}if (parent.keys[107]){key_down_add();}if (parent.keys[13]){key_down_enter();}if (parent.keys[109]){key_down_subtract();}if (parent.keys[110]){key_down_decimal();}if (parent.keys[111]){key_down_divide();}if (parent.keys[112]){key_down_f1();}if (parent.keys[113]){key_down_f2();}if (parent.keys[114]){key_down_f3();}if (parent.keys[115]){key_down_f4();}if (parent.keys[116]){key_down_f5();}if (parent.keys[117]){key_down_f6();}if (parent.keys[118]){key_down_f7();}if (parent.keys[119]){key_down_f8();}if (parent.keys[120]){key_down_f9();}if (parent.keys[122]){key_down_f11();}if (parent.keys[123]){key_down_f12();}if (parent.keys[124]){key_down_f13();}if (parent.keys[125]){key_down_f14();}if (parent.keys[126]){key_down_f15();}if (parent.keys[8]){key_down_backspace();}if (parent.keys[9]){key_down_tab();}if (parent.keys[13]){key_down_enter();}if (parent.keys[16]){key_down_shift();}if (parent.keys[17]){key_down_control();}if (parent.keys[20]){key_down_caps_lock();}if (parent.keys[27]){key_down_esc();}if (parent.keys[32]){key_down_spacebar();}if (parent.keys[33]){key_down_page_up();}if (parent.keys[34]){key_down_page_down();}if (parent.keys[35]){key_down_end();}if (parent.keys[36]){key_down_home();}if (parent.keys[37]){key_down_left_arrow();}if (parent.keys[38]){key_down_up_arrow();}if (parent.keys[39]){key_down_right_arrow();}if (parent.keys[40]){key_down_down_arrow();}if (parent.keys[45]){key_down_insert();}if (parent.keys[46]){key_down_delete();}if (parent.keys[144]){key_down_num_lock();}if (parent.keys[145]){key_down_scrlk();}if (parent.keys[19]){key_down_pause_break();}
  }
  public function _update_timers() {
  	for (i in 0...10){
  	  if (this.timers[i]>0){
    	  this.timers[i] -= 1;
    	  if (this.timers[i] == 0){
    	    Reflect.callMethod(this, Reflect.field(this, "timer_"+Std.string(i)),[]);
    	  }
    	}
  	}
  }
  
  public function collidesWith(other:ImageSprite){
    var sw = this.bm.bitmapData.width;
    var sh = this.bm.bitmapData.height;
    var ow = other.bm.bitmapData.width;
    var oh = other.bm.bitmapData.height;
    var s = this;
    var o = other;
    return new flash.geom.Rectangle(s.x-sw/2,s.y-sh/2,sw,sh).intersects(new flash.geom.Rectangle(o.x-ow/2,o.y-oh/2,ow,oh));
    /**return ((o.y - oh/2 < s.y - sh/2 && s.y - sh/2 < o.y + oh/2) || 
      (s.y - sh/2 < o.y - oh/2 && o.y - oh/2 < s.y + sh/2)) &&
    ((s.x - sw/2 < o.x - ow/2 && o.x - ow/2 < s.x + sw/2) || 
    (o.x - ow/2 < s.x - sw/2 && s.x - sw/2 < o.x + ow/2));**/
    //return this._sprite.hitTestObject(other._sprite);
  }

  public function mouse_down(e : flash.events.MouseEvent){}
  public function mouse_up(e : flash.events.MouseEvent){}
  public function mouse_wheel(e : flash.events.MouseEvent){}
  public function mouse_move(e : flash.events.MouseEvent){}
  public function key_down(e : flash.events.KeyboardEvent){}
  public function _key_down(e : flash.events.KeyboardEvent){
    key_down(e);
    switch(e.keyCode){
      case 48:  key_press_0();case 49:  key_press_1();case 50:  key_press_2();case 51:  key_press_3();case 52:  key_press_4();case 53:  key_press_5();case 54:  key_press_6();case 55:  key_press_7();case 56:  key_press_8();case 57:  key_press_9();case 65:  key_press_a();case 66:  key_press_b();case 67:  key_press_c();case 68:  key_press_d();case 69:  key_press_e();case 70:  key_press_f();case 71:  key_press_g();case 72:  key_press_h();case 73:  key_press_i();case 74:  key_press_j();case 75:  key_press_k();case 76:  key_press_l();case 77:  key_press_m();case 78:  key_press_n();case 79:  key_press_o();case 80:  key_press_p();case 81:  key_press_q();case 82:  key_press_r();case 83:  key_press_s();case 84:  key_press_t();case 85:  key_press_u();case 86:  key_press_v();case 87:  key_press_w();case 88:  key_press_x();case 89:  key_press_y();case 90:  key_press_z();case 96:  key_press_numpad_0();case 97:  key_press_numpad_1();case 98:  key_press_numpad_2();case 99:  key_press_numpad_3();case 100:  key_press_numpad_4();case 101:  key_press_numpad_5();case 102:  key_press_numpad_6();case 103:  key_press_numpad_7();case 104:  key_press_numpad_8();case 105:  key_press_numpad_9();case 106:  key_press_multiply();case 107:  key_press_add();case 109:  key_press_subtract();case 110:  key_press_decimal();case 111:  key_press_divide();case 112:  key_press_f1();case 113:  key_press_f2();case 114:  key_press_f3();case 115:  key_press_f4();case 116:  key_press_f5();case 117:  key_press_f6();case 118:  key_press_f7();case 119:  key_press_f8();case 120:  key_press_f9();case 122:  key_press_f11();case 123:  key_press_f12();case 124:  key_press_f13();case 125:  key_press_f14();case 126:  key_press_f15();case 8:  key_press_backspace();case 9:  key_press_tab();case 13:  key_press_enter();case 16:  key_press_shift();case 17:  key_press_control();case 20:  key_press_caps_lock();case 27:  key_press_esc();case 32:  key_press_spacebar();case 33:  key_press_page_up();case 34:  key_press_page_down();case 35:  key_press_end();case 36:  key_press_home();case 37:  key_press_left_arrow();case 38:  key_press_up_arrow();case 39:  key_press_right_arrow();case 40:  key_press_down_arrow();case 45:  key_press_insert();case 46:  key_press_delete();case 144:  key_press_num_lock();case 145:  key_press_scrlk();case 19:  key_press_pause_break();
    }
  }
  public function key_up(e : flash.events.KeyboardEvent){}
  public function _key_up(e : flash.events.KeyboardEvent){
    key_up(e);
    switch(e.keyCode){
      case 48:  key_release_0();case 49:  key_release_1();case 50:  key_release_2();case 51:  key_release_3();case 52:  key_release_4();case 53:  key_release_5();case 54:  key_release_6();case 55:  key_release_7();case 56:  key_release_8();case 57:  key_release_9();case 65:  key_release_a();case 66:  key_release_b();case 67:  key_release_c();case 68:  key_release_d();case 69:  key_release_e();case 70:  key_release_f();case 71:  key_release_g();case 72:  key_release_h();case 73:  key_release_i();case 74:  key_release_j();case 75:  key_release_k();case 76:  key_release_l();case 77:  key_release_m();case 78:  key_release_n();case 79:  key_release_o();case 80:  key_release_p();case 81:  key_release_q();case 82:  key_release_r();case 83:  key_release_s();case 84:  key_release_t();case 85:  key_release_u();case 86:  key_release_v();case 87:  key_release_w();case 88:  key_release_x();case 89:  key_release_y();case 90:  key_release_z();case 96:  key_release_numpad_0();case 97:  key_release_numpad_1();case 98:  key_release_numpad_2();case 99:  key_release_numpad_3();case 100:  key_release_numpad_4();case 101:  key_release_numpad_5();case 102:  key_release_numpad_6();case 103:  key_release_numpad_7();case 104:  key_release_numpad_8();case 105:  key_release_numpad_9();case 106:  key_release_multiply();case 107:  key_release_add();case 109:  key_release_subtract();case 110:  key_release_decimal();case 111:  key_release_divide();case 112:  key_release_f1();case 113:  key_release_f2();case 114:  key_release_f3();case 115:  key_release_f4();case 116:  key_release_f5();case 117:  key_release_f6();case 118:  key_release_f7();case 119:  key_release_f8();case 120:  key_release_f9();case 122:  key_release_f11();case 123:  key_release_f12();case 124:  key_release_f13();case 125:  key_release_f14();case 126:  key_release_f15();case 8:  key_release_backspace();case 9:  key_release_tab();case 13:  key_release_enter();case 16:  key_release_shift();case 17:  key_release_control();case 20:  key_release_caps_lock();case 27:  key_release_esc();case 32:  key_release_spacebar();case 33:  key_release_page_up();case 34:  key_release_page_down();case 35:  key_release_end();case 36:  key_release_home();case 37:  key_release_left_arrow();case 38:  key_release_up_arrow();case 39:  key_release_right_arrow();case 40:  key_release_down_arrow();case 45:  key_release_insert();case 46:  key_release_delete();case 144:  key_release_num_lock();case 145:  key_release_scrlk();case 19:  key_release_pause_break();
    }
  }
  public function timer_0(){}
  public function timer_1(){}
  public function timer_2(){}
  public function timer_3(){}
  public function timer_4(){}
  public function timer_5(){}
  public function timer_6(){}
  public function timer_7(){}
  public function timer_8(){}
  public function timer_9(){}
  public function off_of_map(){}
  public function create(){}
  public function created(){}
  public function destroy(){}
  public function collide(other:BaseObject){}
  public function step(){}
  // all the keys
  public function key_down_0(){} public function key_press_0(){} public function key_release_0(){} public function key_down_1(){} public function key_press_1(){} public function key_release_1(){} public function key_down_2(){} public function key_press_2(){} public function key_release_2(){} public function key_down_3(){} public function key_press_3(){} public function key_release_3(){} public function key_down_4(){} public function key_press_4(){} public function key_release_4(){} public function key_down_5(){} public function key_press_5(){} public function key_release_5(){} public function key_down_6(){} public function key_press_6(){} public function key_release_6(){} public function key_down_7(){} public function key_press_7(){} public function key_release_7(){} public function key_down_8(){} public function key_press_8(){} public function key_release_8(){} public function key_down_9(){} public function key_press_9(){} public function key_release_9(){} public function key_down_a(){} public function key_press_a(){} public function key_release_a(){} public function key_down_b(){} public function key_press_b(){} public function key_release_b(){} public function key_down_c(){} public function key_press_c(){} public function key_release_c(){} public function key_down_d(){} public function key_press_d(){} public function key_release_d(){} public function key_down_e(){} public function key_press_e(){} public function key_release_e(){} public function key_down_f(){} public function key_press_f(){} public function key_release_f(){} public function key_down_g(){} public function key_press_g(){} public function key_release_g(){} public function key_down_h(){} public function key_press_h(){} public function key_release_h(){} public function key_down_i(){} public function key_press_i(){} public function key_release_i(){} public function key_down_j(){} public function key_press_j(){} public function key_release_j(){} public function key_down_k(){} public function key_press_k(){} public function key_release_k(){} public function key_down_l(){} public function key_press_l(){} public function key_release_l(){} public function key_down_m(){} public function key_press_m(){} public function key_release_m(){} public function key_down_n(){} public function key_press_n(){} public function key_release_n(){} public function key_down_o(){} public function key_press_o(){} public function key_release_o(){} public function key_down_p(){} public function key_press_p(){} public function key_release_p(){} public function key_down_q(){} public function key_press_q(){} public function key_release_q(){} public function key_down_r(){} public function key_press_r(){} public function key_release_r(){} public function key_down_s(){} public function key_press_s(){} public function key_release_s(){} public function key_down_t(){} public function key_press_t(){} public function key_release_t(){} public function key_down_u(){} public function key_press_u(){} public function key_release_u(){} public function key_down_v(){} public function key_press_v(){} public function key_release_v(){} public function key_down_w(){} public function key_press_w(){} public function key_release_w(){} public function key_down_x(){} public function key_press_x(){} public function key_release_x(){} public function key_down_y(){} public function key_press_y(){} public function key_release_y(){} public function key_down_z(){} public function key_press_z(){} public function key_release_z(){} public function key_down_numpad_0(){} public function key_press_numpad_0(){} public function key_release_numpad_0(){} public function key_down_numpad_1(){} public function key_press_numpad_1(){} public function key_release_numpad_1(){} public function key_down_numpad_2(){} public function key_press_numpad_2(){} public function key_release_numpad_2(){} public function key_down_numpad_3(){} public function key_press_numpad_3(){} public function key_release_numpad_3(){} public function key_down_numpad_4(){} public function key_press_numpad_4(){} public function key_release_numpad_4(){} public function key_down_numpad_5(){} public function key_press_numpad_5(){} public function key_release_numpad_5(){} public function key_down_numpad_6(){} public function key_press_numpad_6(){} public function key_release_numpad_6(){} public function key_down_numpad_7(){} public function key_press_numpad_7(){} public function key_release_numpad_7(){} public function key_down_numpad_8(){} public function key_press_numpad_8(){} public function key_release_numpad_8(){} public function key_down_numpad_9(){} public function key_press_numpad_9(){} public function key_release_numpad_9(){} public function key_down_multiply(){} public function key_press_multiply(){} public function key_release_multiply(){} public function key_down_add(){} public function key_press_add(){} public function key_release_add(){} public function key_down_enter(){} public function key_press_enter(){} public function key_release_enter(){} public function key_down_subtract(){} public function key_press_subtract(){} public function key_release_subtract(){} public function key_down_decimal(){} public function key_press_decimal(){} public function key_release_decimal(){} public function key_down_divide(){} public function key_press_divide(){} public function key_release_divide(){} public function key_down_f1(){} public function key_press_f1(){} public function key_release_f1(){} public function key_down_f2(){} public function key_press_f2(){} public function key_release_f2(){} public function key_down_f3(){} public function key_press_f3(){} public function key_release_f3(){} public function key_down_f4(){} public function key_press_f4(){} public function key_release_f4(){} public function key_down_f5(){} public function key_press_f5(){} public function key_release_f5(){} public function key_down_f6(){} public function key_press_f6(){} public function key_release_f6(){} public function key_down_f7(){} public function key_press_f7(){} public function key_release_f7(){} public function key_down_f8(){} public function key_press_f8(){} public function key_release_f8(){} public function key_down_f9(){} public function key_press_f9(){} public function key_release_f9(){} public function key_down_f11(){} public function key_press_f11(){} public function key_release_f11(){} public function key_down_f12(){} public function key_press_f12(){} public function key_release_f12(){} public function key_down_f13(){} public function key_press_f13(){} public function key_release_f13(){} public function key_down_f14(){} public function key_press_f14(){} public function key_release_f14(){} public function key_down_f15(){} public function key_press_f15(){} public function key_release_f15(){} public function key_down_backspace(){} public function key_press_backspace(){} public function key_release_backspace(){} public function key_down_tab(){} public function key_press_tab(){} public function key_release_tab(){}   /*public function key_down_enter(){}   public function key_press_enter(){}   public function key_release_enter(){}*/ public function key_down_shift(){} public function key_press_shift(){} public function key_release_shift(){} public function key_down_control(){} public function key_press_control(){} public function key_release_control(){} public function key_down_caps_lock(){} public function key_press_caps_lock(){} public function key_release_caps_lock(){} public function key_down_esc(){} public function key_press_esc(){} public function key_release_esc(){} public function key_down_spacebar(){} public function key_press_spacebar(){} public function key_release_spacebar(){} public function key_down_page_up(){} public function key_press_page_up(){} public function key_release_page_up(){} public function key_down_page_down(){} public function key_press_page_down(){} public function key_release_page_down(){} public function key_down_end(){} public function key_press_end(){} public function key_release_end(){} public function key_down_home(){} public function key_press_home(){} public function key_release_home(){} public function key_down_left_arrow(){} public function key_press_left_arrow(){} public function key_release_left_arrow(){} public function key_down_up_arrow(){} public function key_press_up_arrow(){} public function key_release_up_arrow(){} public function key_down_right_arrow(){} public function key_press_right_arrow(){} public function key_release_right_arrow(){} public function key_down_down_arrow(){} public function key_press_down_arrow(){} public function key_release_down_arrow(){} public function key_down_insert(){} public function key_press_insert(){} public function key_release_insert(){} public function key_down_delete(){} public function key_press_delete(){} public function key_release_delete(){} public function key_down_num_lock(){} public function key_press_num_lock(){} public function key_release_num_lock(){} public function key_down_scrlk(){} public function key_press_scrlk(){} public function key_release_scrlk(){} public function key_down_pause_break(){} public function key_press_pause_break(){} public function key_release_pause_break(){}

  public function limitPos(x:Int,y:Int,w:Int,h:Int,?margin = 0,?bounce = false){
  	if (this.x<x+margin){
  		this.x = x+margin;
  		if (bounce)this._velocity.bounce_off(90);
  		else
  		  this.hspeed = 0;
  	}
  	if (this.y<y+margin){
  		this.y = y+margin;
  		if (bounce)this._velocity.bounce_off(0);
  		else
  		  this.vspeed = 0;
  	}
  	if (this.x>this.parent.size[0]-margin){
  		this.x = this.parent.size[0]-margin;
  		if (bounce)this._velocity.bounce_off(90);
  		else
  		  this.hspeed = 0;
  	}
  	if (this.y>this.parent.size[1]-margin){
  		this.y = this.parent.size[1]-margin;
  		if (bounce)this._velocity.bounce_off(0);
  		else
  		  this.vspeed = 0;
  	}
  }
  public function _update(){
    if (this.image!=""){
      var bd : BitmapData = cast(ImageSprite.imageCache.get(this._image.subimages[Std.int(this.imagepos)]), BitmapData);
      this.bm.bitmapData = bd;
      this.bm.x = -bd.width/2;
      this.bm.y = -bd.height/2;
      this._sprite.x = this.x;
      this._sprite.y = this.y;
      this._sprite.rotation=this.rotation;
      this._sprite.alpha = this.opacity;
      //trace(this.opacity);
    }
  }
  
  public function wrapPosition(x:Int,y:Int,w:Int,h:Int,vhb:String){
    var width = this.bm.bitmapData.width/2;
    var height = this.bm.bitmapData.height/2;
    
    if (vhb == 'horizontal' || vhb == 'both'){
    	if (this.x<x){
    		this.x = w;
    	}
    	if (this.x>w){
    		this.x = x;
    	}
  	}
    if (vhb == 'vertical' || vhb == 'both'){
    	if (this.y<y){
    		this.y = h;
    	}
    	if (this.y>h){
    		this.y = y;
    	}
  	}
  }
  
  public function wrapPositionToScreen(vhb:String){
    this.wrapPosition(0,0,parent.size[0],parent.size[1],vhb);
  }
}
/**
class ImageSprite extends Sprite {
  
  public override function _step(){
    super._step();
    try{
    for (typ in this.collisions.iterator()){
    	for (obj in this.parent.objects.iterator()){
    	  if (obj == this || Type.getClass(obj) != this.parent.objectdict.get(typ))continue;
    	  if (this.collidesWith(obj)){
    	    Reflect.callMethod(this, Reflect.field(this, "collide_"+typ),[obj]);
    	  }
    	}
    }
    }catch(e:String){this.parent.log += ''+e;}
    this._update();
  	for (obj in this.parent.objects.iterator()){
  	  if (obj == this)continue;
  	  if (this.collidesWith(obj)){
  	    this.collide(obj);
  	  }
  	}
  }
  
  public function image():BitmapData {
      return ImageSprite.imageCache.get(this._image.subimages[Std.int(this.imagepos)]);
  }
  
  public override function draw(screen : flash.display.BitmapData){
    this._update();
    
  }
  
  public override function limitPos(x:Int,y:Int,w:Int,h:Int,?margin = 1,?bounce = false){
    margin=0;
    var width = this.image().width/2;
    var height = this.image().height/2;
  	if (this.x<x+height+margin){
  		this.x = x+height+margin;
  		if (bounce)this._velocity.bounce_off(Math.PI/2);
  	}
  	if (this.y<y+height+margin){
  		this.y = y+height+margin;
  		if (bounce)this._velocity.bounce_off(0);
  	}
  	if (this.x>this.parent.size[0]-width-margin){
  		this.x = this.parent.size[0]-margin-width;
  		if (bounce)this._velocity.bounce_off(Math.PI/2);
  	}
  	if (this.y>this.parent.size[1]-height-margin){
  		this.y = this.parent.size[1]-margin-height;
  		if (bounce)this._velocity.bounce_off(0);
  	}
  }
  
  
  
  public function collidesRect(other:ImageSprite){
    this._update();
    return this.collidesWith(other);
    if (this.x<=other.x && other.x<=this.x+this.image().width || other.x<=this.x && this.x<=other.x+other.image().width){
      if (this.y<=other.y && other.y<=this.y+this.image().height || other.y<=this.y && this.y<=other.y+other.image().height){
        return true;
      }
    }
    return false;
  }
  
  public function limitPosToScreen(bounce:Bool){
    this.limitPos(0,0,parent.size[0],parent.size[1],0,bounce);
  }
}*/

