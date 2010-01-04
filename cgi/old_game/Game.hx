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
import game.BaseSprite;

typedef MapItem = {
  var name : String;
  var x : Int;
  var y : Int;
}

typedef Map = {
  var name : String;
  var persistant : Bool;
  var size : Array<Int>;
  var items : Array<MapItem>;
}

typedef Image = {
  var name : String;
  var subs : Array<String>;
  var speed : Float;
}

class Game extends flash.display.Sprite {
    public var screen : BitmapData;
    public var _root : flash.display.MovieClip;
    public var objects : List<BaseSprite>;
    public var size : Array<Int>;
    public var keys : Array<Bool>;
    public var map : Map;
    public var maps: Hash<Map>;
    public var objectdict : Hash<Class<BaseSprite>>;
    public var images : Hash<Image>;
    public var log : String;
    public var startingmap : String;
    public var loadcount : Int;
    private var _logger : flash.text.TextField;
    
    public function new(images:Hash<Image>, objects:Hash<Class<BaseSprite>>, maps:Hash<Map>, _startingmap:String){
        super();
        flash.Lib.current.addChild(this);
        this._root = flash.Lib.current;
        this.startingmap = _startingmap;
        this.objects = new List<BaseSprite>();
        this.objectdict = objects;
        this.keys = [];
        this.log = 'No Errors';
        this._logger = new flash.text.TextField();
        this._logger.text = this.log;
        this.addChild(this._logger);
        this._logger.x = 0;
        this._logger.y = 0;
        this._logger.height = 500;
        this._logger.width = 300;
        this._logger.textColor = Color.rgb(255,0,0);
        this._logger.thickness = 2.5;
        this.registerEvents();
        this.maps = maps;
        this.images = images;
        if (ImageSprite.imageCache==null)
            ImageSprite.imageCache = new Hash<BitmapData>();
        this.loadcount = 0;
        for (img in this.images.keys()){
          for (sub in this.images.get(img).subs){
            this.loadcount += 1;
            //this.trace('loading '+this.loadcount+' images...');
            ImageSprite.loadImage(sub,this.loadDone,this.trace);
          }
        }
        
        //this.load_map(startingmap);
    }
    
    public function loadDone(){
      this.loadcount -= 1;
      //this.trace('loading '+this.loadcount+' images...');
      if (this.loadcount <= 0){
        this.load_map(this.startingmap);
      }
    }
        
    function registerEvents(){
        this._root.addEventListener(flash.events.Event.ENTER_FRAME,loop);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_DOWN,this.mouseDown);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_UP,this.mouseUp);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_MOVE,this.mouseMove);
        this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_WHEEL,this.mouseWheel);
        this._root.stage.addEventListener(flash.events.KeyboardEvent.KEY_DOWN,this.keyDown);
        this._root.stage.addEventListener(flash.events.KeyboardEvent.KEY_UP,this.keyUp);
    }
    
    function load_map(mapname:String){
          try{
            this.map = this.maps.get(mapname);
            this.size = this.map.size;
            for (i in this.map.items){
            //this.trace('adding an item '+i.name);
              this.objects.push(Type.createInstance(this.objectdict.get(i.name),[this,new Point(i.x,i.y)]));
            }
          }catch(e:Error){
            this.trace(e.name+': '+e.message);
          }
    }
    
    function loop(_){
        step();
        draw();
    }
    
    function step(){
        this._logger.text = this.log;
        for (obj in this.objects.iterator()){
          try{
            obj._step();
          }catch(e:Error){
            this.log = e.name+': '+e.message+'\n'+this.log;
          }
        }
    }
    
    function draw(){
      
      this.screen.fillRect(new Rectangle(0,0,640,480),0xe0e0ff);
      for (obj in this.objects.iterator()){
          obj.draw(this.screen);
      }
    }
    
    public function add(o: BaseSprite){
      this.objects.push(o);
    }
    
    public function remove(o : BaseSprite){
      //if (this.objects.
      this.objects.remove(o);
      o.destroy();
      this.removeChild(o.sprite);
    }
    
    public function trace(str:String){
      this.log = str+'\n'+this.log;
      this.ulog();
    }
    
    function ulog(){
      this._logger.text = this.log;
    }
    
    function mouseDown(e : flash.events.MouseEvent){
        for (obj in this.objects.iterator()){obj.mouse_down(e);}
    }
    function mouseUp(e : flash.events.MouseEvent){
        for (obj in this.objects.iterator()){obj.mouse_up(e);}
    }
    function mouseWheel(e : flash.events.MouseEvent){
        for (obj in this.objects.iterator()){obj.mouse_wheel(e);}
    }
    function mouseMove(e : flash.events.MouseEvent){
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


