import game.Game;
import game.Vector;
import game.BaseObject;
import flash.geom.Point;
import flash.events.Event;
import flash.display.BitmapData;
import flash.display.Loader;
import flash.net.URLRequest;
import flash.ui.Keyboard;

%(plugins_more)s

class %(name)s {
  static function main(){
    var objects:Hash<Class<BaseObject>> = new Hash<Class<BaseObject>>();
%(objects)s
    var maps:Hash<Map> = new Hash<Map>();
%(maps)s
    var images:Hash<Image> = new Hash<Image>();
%(images)s
    var game = new Game(images,objects,maps,"%(maps_more)s",%(width)s,%(height)s);
  }
}

%(objects_more)s

