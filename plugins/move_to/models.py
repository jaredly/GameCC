from django.db import models

from gcc_objects.models import *

from gcc_objects import fields

class Move_To(Action):
    x = fields.PositionField()
    y = fields.PositionField()
    relative = fields.BooleanField()
    target = fields.TargetField()

    TYPE = None
    ICON = {'sheet':'allplugins.png','x':0,'y':1}
    ARG_ORDER = 'x','y','relative'
    METHODS = {
        'python':'''\
def move_to(self, x, y, relative):
    if relative:
        x += self.x
        y += self.y
    self.x = x
    self.y = y
''',
        'haxe':'''\
public function move_to(x:Float, y:Float, relative:Bool) {
    if (relative){
        this.x += x;
        this.y += y;
    } else {
        this.x = x;
        this.y = y;
    }
}
'''
        'javascript':'''\
move_to:function(self, x, y, relative) {
    if (relative){
        self.x += x;
        self.y += y;
    } else {
        self.x = x;
        self.y = y;
    }
}
'''
    }
    
    def __unicode__(self):
        if self.relative:
            return u'Move to (%s, %s) relatively' % (self.x, self.y)
        return u'Move to (%s, %s)' % (self.x, self.y)

# Create your models here.
