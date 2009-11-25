// Free Ski Tree
// GM2D.com haxe code for simple game.
// I am placing this code, and associated "tiles.png" in the public domain.

// Since we are dealing with flash version 9, the general graphics
//  classes are in the "flash.display" package.
import flash.display.Sprite;
import flash.display.BitmapData;
import flash.display.Bitmap;
import flash.geom.Rectangle;
import flash.geom.Point;
import flash.events.Event;
import flash.events.KeyboardEvent;
import flash.ui.Keyboard;
import flash.text.TextField;
import flash.text.TextFormat;
import flash.filters.GlowFilter;


/*
 The Blob class (BLitter OBject) is a rectangle of pixels that can be
  quickyly and easily copied to the screen.  Perhaps a better name would
  be Sprite, but that would be too confusing.
 The main purpose of this class is to do a "copyPixels", and it just gathers
  the required data together to make this very easy.
*/
class Blob
{
   var mArena:BitmapData;
   var mBits:BitmapData;
   var mRect:Rectangle;
   var mPoint:Point;
   // The "hotspot" is the logical origin of the object, with respect
   //  to the top left of its bitmap rectangle.  This allows you to deal
   //  with the position of the object, without having to worry about drawing
   //  offsets etc.
   var mHotX:Float;
   var mHotY:Float;

   // Passing the arena into the constructor is not really required,
   //  but doing this reduces the number of params we have to pass into
   //  the Draw function;
   public function new(inArena:BitmapData,inBits:BitmapData,inX:Int, inY:Int, inW:Int, inH:Int,
           ?inHotX:Null<Float>, ?inHotY:Null<Float>)
   {
      mArena = inArena;
      mBits = inBits;
      mRect = new Rectangle(inX,inY,inW,inH);
      mPoint = new Point(0,0);
      // If null is provided, assume the centre.
      mHotX = inHotX==null ? inW/2 : inHotX;
      mHotY = inHotY==null ? inH/2 : inHotY;
   }
   public function draw(inX:Float,inY:Float)
   {
      mPoint.x = inX-mHotX;
      mPoint.y = inY-mHotY;
      mArena.copyPixels(mBits,mRect,mPoint,null,null,true);
   }
}

// All games would probably have some kind of state like this...
enum SkiState { FirstRun; Playing; Dead; }

// Array of the x-coordinate of the trees.
typedef TreeRow = Array<Float>;

// This is our main class, and in this case, it contains the whole game.
// It extends the standard flash "Sprite" class, which allows child objects
//  and events.  No need for a MovieClip, because we are not using the flash
//  timelining code.
class Ski extends Sprite
{
   // Using "copyPixels" we draw into this bitmap...
   var mArena:BitmapData;

   // What to do on an update...
   var mState : SkiState;

   // Our basic drawing objects
   var mTree:Blob;
   var mPlayerDown:Blob;
   var mPlayerLeft:Blob;
   var mPlayerRight:Blob;

   // Contains the state (whether currently pressed/down) of every key
   var mKeyDown:Array<Bool>;

   // Time of last step - for calculating time deltas...
   var mLastStep:Float;

   // We increate game speed by increasing steps-per-second.
   // Note that this is independent of the flash frame rate, since we can
   //  do multiple steps per flash redraw.
   var mStepsPerSecond:Float;

   // An array of trees to ski past.  Other arrangements are possible,
   //  for example only traking the visible trees and creating new
   //  ones randomly as we go
   var mTrees:Array<TreeRow>;

   // All position are in "field" coordinates, which are logical pixels.
   // We use the modulo operator (%) to wrap the trees around
   static var mFieldHeight = 10000;
   var mPlayerX:Float;
   var mPlayerY:Float;

   // Curreny play
   var mScore:Float;
   // Current session
   var mTopScore:Float;
   // GUI items
   var mScoreText:TextField;
   var mTopScoreText:TextField;


   // All the graphics are provided in the input image (BitmapData).
   function new(inBitmap:BitmapData)
   {
      // Since this class inherits from Sprite, we must call this.
      super();
      flash.Lib.current.addChild(this);
      mKeyDown = [];
      mArena = new BitmapData(640,480);
      addChild(new Bitmap(mArena) );

      mTree = new Blob(mArena,inBitmap,4,0,54,64,null,62);
      mPlayerLeft = new Blob(mArena,inBitmap,110,16,26,40);
      mPlayerDown = new Blob(mArena,inBitmap,70,12,26,46);
      mPlayerRight = new Blob(mArena,inBitmap,148,16,26,40);

      stage.addEventListener(KeyboardEvent.KEY_DOWN, OnKeyDown );
      stage.addEventListener(KeyboardEvent.KEY_UP, OnKeyUp );
      stage.addEventListener(Event.ENTER_FRAME, OnEnter);

      // Allocate row
      mTrees = [];
      mTrees[mFieldHeight-1] = null;

      // Fill up tree array.
      // This will be constant throughout the session, so the player can learn
      //  the best way down.  A random number "seed" could be used if you wanted
      //  the game to be the same on different machines.
      for(i in 0...500)
      {
         // Randomise x position.  Make sure they overlap the edges so that
         //  there is no advantage from shooting down the edge.
         var x = (Math.random()*700)-30;
         // Leave a gap for the top 250 rows so the player can start in piece.
         var y = Std.int(Math.random()*(mFieldHeight-250)) + 250;
         if (mTrees[y]==null)
            mTrees[y] = [];
         mTrees[y].push(x);
      }


      // The "GUI" consists of two TextFields overlapping the arena.
      // These do not use "copyPixels", but take advantage of some of the
      //  other benefits provided by flash display list model.
      // In a "real" game, you should use a custom embedded font, rather than
      //  some crappy default.
      mScoreText = new TextField();
      mScoreText.x = 10;
      mScoreText.y = 10;
      var format:TextFormat = new TextFormat();
      format.font = "Arial";
      format.bold = true;
      format.color = 0xffffff;
      format.size = 20;
      mScoreText.defaultTextFormat = format;
      mScoreText.text = "Score:0";
      mScoreText.width = 640;
      mScoreText.filters = [ new  GlowFilter(0x0000ff, 1.0, 3, 3, 3, 3, false, false) ];
      addChild(mScoreText);

      mTopScoreText = new TextField();
      mTopScoreText.x = 100;
      mTopScoreText.y = 10;
      format.color = 0xffffff;
      mTopScoreText.defaultTextFormat = format;
      mTopScoreText.filters = [ new  GlowFilter(0xff0000, 1.0, 3, 3, 3, 3, false, false) ];
      addChild(mTopScoreText);

      // Just something small to aspire too...
      mTopScore = 0;
      CheckTopScore(1000);

      mLastStep = haxe.Timer.stamp();

      Reset();
      // Slightly different message at the beginning
      mState = SkiState.FirstRun;
   }

   // Update the top score at the end of the game, if required.
   function CheckTopScore(inScore:Float)
   {
      if (inScore>mTopScore)
      {
         mTopScore = inScore;
         var s = Std.int(mTopScore * 0.1);
         mTopScoreText.text = "TopScore:" + s + "0";
         var w = mTopScoreText.textWidth;
         mTopScoreText.width = w + 20;
         mTopScoreText.x = 620 - w;
      }
   }

   // Get ready to start the game again
   function Reset()
   {
      mPlayerX = 320;
      mPlayerY = 20;
      mScore = 0;
      mStepsPerSecond = 100;
   }

   // Update one step.
   // Is this case, we will descend one line.
   // When the game speeds up, this will get called more often.
   function Update()
   {
      // Actually need to move down ?
      if (mState==SkiState.Playing)
      {
         // This small bit of code defined the whole "mechanic" of the game.
         // Other things could be done here, eg acceleration or a "one button"
         //  mode where you either go left-or-right, but not down.
         // Also, mouse support could be added here.
         var dx = mKeyDown[ Keyboard.LEFT ] ? -1 :
                  mKeyDown[ Keyboard.RIGHT ] ? 1 : 0;
         // This effectively defines the angle you go at when you turn
         mPlayerX += dx * 0.3;
         // Limit to screen
         if (mPlayerX<12) mPlayerX = 12;
         if (mPlayerX>628) mPlayerX = 628;
         // Going down...
         mPlayerY += 1;
         // Loop around, to keep numbers from overflowing.
         if (mPlayerY > mFieldHeight)
            mPlayerY -= mFieldHeight;
         // 1 Point per row
         mScore += 1.0;

         // Get faster as we get more points
         mStepsPerSecond = 100 + mScore * 0.01;

         // Check death...
         var row = mTrees[Std.int(mPlayerY)];
         if (row!=null)
            for(x in row)
               if ( Math.abs(x-mPlayerX) < 15 )
               {
                  // We are dead.  Stop scoring.
                  CheckTopScore(mScore);
                  mState = SkiState.Dead;
               }
      }
   }

   // Update the graphics based on class variables.
   // Note that this will be called less frequently than the "Update" call.
   // inExtra is not used in this example, because scrolling seems smooth enough.
   function Render(inExtra:Float)
   {
      // Offset all the object to keep th apparent position on the player
      //  the same.  This creates a "virtual viewport" for rendering.
      var scroll_y = mPlayerY - 60;

      // The "copyPixels" method works by clearing the buffer and then drawing
      //  the bitmaps into the offscreen buffer.
      mArena.fillRect(new Rectangle(0,0,640,480),0xe0e0ff);

      var blob = mKeyDown[ Keyboard.LEFT ] ? mPlayerLeft :
                 mKeyDown[ Keyboard.RIGHT ] ? mPlayerRight :
                                             mPlayerDown;
      blob.draw(mPlayerX, mPlayerY - scroll_y);

      // These bounds ensure the to and the bottom of all potentially visible
      //  sprites are rendered.
      for(y in -10...(480+80))
      {
         // Given the pixel position, back-calculate the field row position
         //  based on the scroll position.
         var field_y = Std.int(scroll_y + y) % mFieldHeight;
         var row = mTrees[field_y];
         if (row!=null)
         {
            for(x in row)
               mTree.draw(x,y);
         }
      }

      // Update the gui message.
      if (mState==SkiState.FirstRun)
      {
         mScoreText.text = "Press any key to start";
      }
      else if (mState==SkiState.Playing)
      {
         // Round scores to nearest 10 for display purposes
         var s = Std.int(mScore * 0.1);
         mScoreText.text = "Score:" + s + "0";
      }
      else
      {
         var s = Std.int(mScore * 0.1);
         if (mScore>=mTopScore)
            mScoreText.text = "Top Score! " + s + "0" + "    Press [space] to go again";
         else
            mScoreText.text = "You scored " + s + "0" + "    Press [space] to try again";
      }
   }


   // Respond to a key-down event.
   function OnKeyDown(event:KeyboardEvent)
   {
      // When a key is held down, multiple KeyDown events are generated.
      // This check means we only pick up the first one.
      if (!mKeyDown[event.keyCode])
      {
         // Most of the game runs off the "mKeyDown" state, but the in beginning we
         //  use the transition event...
         if (mState == SkiState.FirstRun)
            mState = SkiState.Playing;
         else if (mState == SkiState.Dead && event.keyCode==Keyboard.SPACE)
         {
            Reset();
            mState = SkiState.Playing;
         }
         // Store for use in game
         mKeyDown[event.keyCode] = true;
      }
   }

   // Key-up event
   function OnKeyUp(event:KeyboardEvent)
   {
      // Store for use in game
      mKeyDown[event.keyCode] = false;
   }

   // This function gets called once per flash frame.
   // This will be approximately the rate specified in the swf, but usually a
   //  bit slower.  For accurate timing, we will not rely on flash to call us
   //  consistently, but we will do our own timing.
   function OnEnter(e:flash.events.Event)
   {
      var now = haxe.Timer.stamp();
      // Do a number of descrete steps based on the mStepsPerSecond.
      var steps = Math.floor( (now-mLastStep) * mStepsPerSecond );
      // Since the mStepsPerSecond may change in the Update call, make sure
      //  we do all our calculations before we call Update.
      mLastStep += steps / mStepsPerSecond;
      var fractional_step = (now-mLastStep) * mStepsPerSecond;

      for(i in 0...steps)
         Update();

      // This helps flash efficiently update the bitmap, batching the changes
      mArena.lock();

      // fractional_step is something we don't use, but it could be used to do some
      //  dead-reckoning in the render code to smooth out the display.
      Render(fractional_step);

      // This completes the batching
      mArena.unlock();
   }



   // Haxe will always look for a static function called "main".
   static public function main()
   {
      // There are a number of ways to get bitmap data into flash.
      // In this case, we're loading it from a file that is placed next to the
      //  game swf.  Other ways will be described later.
      // Since the downloding of the bitmap from a remote location may take some
      //  time, flash uses an asynchronous api to delivier the data.
      //  This means that the request is sent and the data only becomes valid when
      //  the callback is called.  A loading screen would be appropriate here, but
      //  that's beond the scope of this example, as is appropriate error checking.

      // Create the request object...
      var loader = new flash.display.Loader();
      // When the image is ready, instanciate the game class...
      loader.contentLoaderInfo.addEventListener(flash.events.Event.COMPLETE,
          function(_) { new Ski(untyped loader.content.bitmapData); });
      // Fire off the request and wait...
      loader.load(new flash.net.URLRequest("tiles.png"));
   }
}

