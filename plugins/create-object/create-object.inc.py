def createObject(self, object, x, y, relative, direction, speed):
  if relative:
    x+=self.x
    y+=self.y
  obj = self.parent.objectdict[object](self.parent,x,y)
  obj.setV(direction, speed, False)
  self.parent.objects.append(obj)
  obj.created()
