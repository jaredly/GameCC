package game;
import game.Vector;
import game.ObjectBase;
import game.Group;

typedef MapItem = {
  var name : String;
  var x : Int;
  var y : Int;
}

typedef Map = {
  var name : String;
  var persistant : Bool;
  var width :Int;
  var height: Int;
  var fps:Int;
  var items : Array<MapItem>;
}

typedef Image = {
  var name : String;
  var subimages : Array<String>;
  var speed : Float;
}

class GameBase {
  public var images : Hash<Image>;
  public var objectdict : Hash<Class<ObjectBase>>;
  public var maps : Hash<Map>;
  public var raw_images : Array<String>;
  public var size : Array<Int>;
  public var _log : String;
  public var _root : flash.display.MovieClip;
  public var baseobject : Class<ObjectBase>;
  public var imagecache : Hash<flash.display.BitmapData>;
  
  public var map : Map;
  public var fps : Int;
  public var objects : Group;
  public var running : Bool;
  public var mapname : String;
  public var keys : Array<Bool>;
  
  public function new(images : Hash<Image>, objectdict : Hash<Class<ObjectBase>>, maps : Hash<Map>, raw_images : Array<String>, baseobject : Class<ObjectBase>){
    this.images = images;
    this.objectdict = objectdict;
    this.maps = maps;
    this.fps = 40;
    this.raw_images = raw_images;
    this._log = 'Hello Peoples';
    this.baseobject = baseobject;
  }
  public function preload_images(images:Array<String>){
  }
  public function log(what:Dynamic){
    this._log += '\n'+what;
  }
  public function setup_screen(){
  }
  public function test_collisions(){
    //cdct = {};
    /** fix **
    for name, cls in this.objectdict.items(){
      for one in this.objects[cls]{
        for other in cls.collisions{
          for obj in this.objects[this.objectdict[other]]{
            if obj == one{continue;}
            if not cdct.has_key(frozenset([one,obj])){
              cdct[frozenset([one,obj])] = one.collidesWith(obj);
            }
            if cdct[frozenset([one,obj])]{
              getattr(one,'collide_'+other)(obj);
            }
          }
        }
      }
    } **/
  }
  public function registerCallbacks() {
  }
  
  public function start(mapname:String){
    this.setup_screen();
    this.mapname = mapname;
    this.preload_images(this.raw_images);
  }
  public function doneloading() {
    this.load_map(this.mapname);
    this.registerCallbacks();
  }
  public function load_map(mapname:String) {
    this.map = this.maps.get(mapname);
    this.fps = this.map.fps;
    this.size = [this.map.width,this.map.height];
    this.objects = new Group(this.baseobject);
    for (item in this.map.items){
      // redo
      this.objects.append(Type.createInstance(this.objectdict.get(item.name), [item.x, item.y]));
    }
  }
  public function events(){
  }
  public function step(){
    for (obj in this.objects.get(this.baseobject).iterator()){
      obj.step();
    }
    this.test_collisions();
  }
  public function draw(){
  }
}
