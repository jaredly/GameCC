package game;
import game.Vector;
import game.ObjectBase;
import game.Group;

class Object extends ObjectBase {
  public var _sprite : flash.display.Sprite;
  public var bm : flash.display.Bitmap;
  
  public override function setup_image() {
    this._sprite = new flash.display.Sprite();
    this.parent._root.addChild(this._sprite);
    
    this.bm = new flash.display.Bitmap(this.parent.imagecache.get(this._image.subimages[0]));
    this.width = this.parent.imagecache.get(this._image.subimages[0]).width;
    this.height = this.parent.imagecache.get(this._image.subimages[0]).height;
    this.bm.x = -this.width/2;
    this.bm.y = -this.height/2;
    this._sprite.addChild(bm);
  }
  public override function render() {
    this._sprite.x=this.x;
    this._sprite.y=this.y;
    this._sprite.rotation = this._rotation;
    this._sprite.alpha = this._opacity;
    var bd : flash.display.BitmapData = cast(this.parent.imagecache.get(this._image.subimages[Std.int(this.imagepos)]), flash.display.BitmapData);
    this.bm.bitmapData = bd;
    this.width = bd.width;
    this.height = bd.height;
    this.bm.x = -bd.width/2;
    this.bm.y = -bd.height/2;
  }
  public override function collidesWith(other:ObjectBase):Bool{
    var s = this;
    var o = other;
    return ((o.y - o.height/2 < s.y - s.height/2 && s.y - s.height/2 < o.y + o.height/2) || 
      (s.y - s.height/2 < o.y - o.height/2 && o.y - o.height/2 < s.y + s.height/2)) &&
    ((s.x - s.width/2 < o.x - o.width/2 && o.x - o.width/2 < s.x + s.width/2) || 
    (o.x - o.width/2 < s.x - s.width/2 && s.x - s.width/2 < o.x + o.width/2));
  }
}

class Game extends GameBase {
  public var _logger : flash.text.TextField;
  
  public var toload : Int;
  
  public override function preload_images(images:Array<String>){
    toload = images.length;
    for (img in images.iterator()){
      preload_image(img);
    }
  }
  
  public function preload_image(img:String) {
    var that = this;
    var loader : flash.display.Loader = new flash.display.Loader();
    loader.contentLoaderInfo.addEventListener(flash.events.Event.COMPLETE,function(_){
        that.imagecache.set(img,untyped loader.content.bitmapData);
        that.incrementLoad();
    });
    loader.load(new flash.net.URLRequest('../images/'+img));
  }
  
  public function incrementLoad() {
    this.toload -= 1;
    if (this.toload <= 0){
      this.doneloading();
    }
  }
  
  public override function setup_screen(){
    this._root = flash.Lib.current;
    this._logger = new flash.text.TextField();
    this._logger.text = this._log;
    this._root.addChild(this._logger);
    this._logger.x = 0;
    this._logger.y = 0;
    this._logger.height = 500;
    this._logger.width = 300;
    this._logger.textColor = Color.rgb(255,0,0);
    this._logger.thickness = 2.5;
  }
  
  public override function draw(){
    for (obj in this.objects.iterator()){
      obj.render();
    }
    this._logger.text = this._log;
  }
  
  public override function registerCallbacks() {
    this._root.addEventListener(flash.events.Event.ENTER_FRAME,loop);
    this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_DOWN,this.mouseDown);
    this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_UP,this.mouseUp);
    this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_MOVE,this.mouseMove);
    this._root.stage.addEventListener(flash.events.MouseEvent.MOUSE_WHEEL,this.mouseWheel);
    this._root.stage.addEventListener(flash.events.KeyboardEvent.KEY_DOWN,this.keyDown);
    this._root.stage.addEventListener(flash.events.KeyboardEvent.KEY_UP,this.keyUp);
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
  function loop(_){
      step();
      draw();
  }
}

