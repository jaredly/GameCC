package game;
import flash.geom.Point;
import flash.geom.Rectangle;
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
import game.Sprite;
import game.BaseObject;
import game.Group;

typedef MapItem = {
  var name : String;
  var x : Int;
  var y : Int;
}

typedef Map = {
  var name : String;
  var persistant : Bool;
  var width:Int;
  var height:Int;
  var items : Array<MapItem>;
}

typedef Image = {
  var name : String;
  var subimages : Array<String>;
  var speed : Float;
}

class Game extends flash.display.Sprite {
    public var screen : BitmapData;
    public var _root : flash.display.MovieClip;
    public var objects : Group;
    public var size : Array<Int>;
    public var keys : Array<Bool>;
    public var map : Map;
    public var maps: Hash<Map>;
    public var objectdict : Hash<Class<BaseObject>>;
    public var images : Hash<Image>;
    public var log : String;
    public var startingmap : String;
    public var loadcount : Int;
    private var _logger : flash.text.TextField;
    public var mousex : Float;
    public var mousey : Float;
    public var owidth : Int;
    public var oheight : Int;
    public var debug:Int;
    
    public function new(images:Hash<Image>, objects:Hash<Class<BaseObject>>, maps:Hash<Map>, _startingmap:String, width:Int, height:Int){
        debug = 0;
        if (debug>3)trace('initing game');
        super();
        flash.Lib.current.addChild(this);
        this._root = flash.Lib.current;
        this.startingmap = _startingmap;
        this.objects = new Group();
        this.objectdict = objects;
        this.keys = [];
        this.mousex = 0;
        this.mousey = 0;
        this.owidth = width;
        this.oheight = height;
        this.registerEvents();
        this.maps = maps;
        this.images = images;
        if (ImageSprite.imageCache==null)
            ImageSprite.imageCache = new Hash<BitmapData>();
        this.loadcount = 0;
        for (img in this.images.keys()){
          for (sub in this.images.get(img).subimages){
            this.loadcount += 1;
            ImageSprite.loadImage(sub,this.loadDone,debug);
          }
        }
        if (debug>3)trace('inited game');
    }
    
    public function loadDone(){
      this.loadcount -= 1;
      if (this.loadcount <= 0){
        this.load_map(this.startingmap);
      }
    }
        
    function registerEvents(){
        if (debug>3)trace('registering events');
        this._root.addEventListener(flash.events.Event.ENTER_FRAME,loop);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_DOWN,this.mouseDown);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_UP,this.mouseUp);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_MOVE,this.mouseMove);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_WHEEL,this.mouseWheel);
        this._root.stage.addEventListener(flash.events.KeyboardEvent.KEY_DOWN,this.keyDown);
        this._root.stage.addEventListener(flash.events.KeyboardEvent.KEY_UP,this.keyUp);
        if (debug>3)trace('registered events');
    }
    
    function load_map(mapname:String){
        if (debug>3)trace('loading map');
            this.map = this.maps.get(mapname);
            this.size = [this.map.width,this.map.height];
            this.x = this.owidth/2 - this.map.width/2;
            this.y = this.oheight/2 - this.map.height/2;
          try{
            for (i in this.map.items){
              this.objects.append(Type.createInstance(this.objectdict.get(i.name),[this,i.x,i.y]));
            }
          }catch(e:Error){
            trace(e.name+': '+e.message);
          }
        if (debug>3)trace('loaded map');
    }
    
    function loop(_){
      try{
        step();
        draw();
      }catch(e:Error){
        trace(e.name+': '+e.message);
      }
    }
    
    function step(){
      for (obj in this.objects.iterator()){
        try{
          obj._step();
        }catch(e:Error){
          trace(e.name+': '+e.message + ' : '+obj);
        }
      }
      for (cls in this.objectdict.iterator()){
        for (one in this.objects.get(cls)){
          for (other in one.collisions.iterator()){
            for (obj in this.objects.get(this.objectdict.get(other))){
              if (obj == one)continue;
              if (one.collidesWith(obj)){
                Reflect.callMethod(one, Reflect.field(one, 'collide_'+other),[obj]);
              }
            }
          }
        }
      }
    }
    
    function draw(){
      //this.screen.fillRect(new Rectangle(0,0,640,480),0xe0e0ff);
      for (obj in this.objects.iterator()){
        obj.render(this.screen);
      }
    }
    
    public function add(o: BaseObject){
      this.objects.append(o);
    }
    
    public function remove(o : BaseObject){
      this.objects.remove(o);
      this.removeChild(o._sprite);
    }
    
    function ulog(){
      this._logger.text = this.log;
    }
    
    function mouseDown(e : flash.events.MouseEvent){
      this.mousex = e.stageX;this.mousey = e.stageY;
      for (obj in this.objects.iterator()){obj.mouse_down(e);}
    }
    function mouseUp(e : flash.events.MouseEvent){
      this.mousex = e.stageX;this.mousey = e.stageY;
      for (obj in this.objects.iterator()){obj.mouse_up(e);}
    }
    function mouseWheel(e : flash.events.MouseEvent){
      this.mousex = e.stageX;this.mousey = e.stageY;
      for (obj in this.objects.iterator()){obj.mouse_wheel(e);}
    }
    function mouseMove(e : flash.events.MouseEvent){
      this.mousex = e.stageX;this.mousey = e.stageY;
      for (obj in this.objects.iterator()){obj.mouse_move(e);}
    }
    function keyDown(e : flash.events.KeyboardEvent){
        this.keys[e.keyCode] = true;
        for (obj in this.objects.iterator()){obj._key_down(e);}
    }
    function keyUp(e : flash.events.KeyboardEvent){
        this.keys[e.keyCode] = false;
        for (obj in this.objects.iterator()){obj._key_up(e);}
    }
}


