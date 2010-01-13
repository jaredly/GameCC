def collisionAt(self, x, y, object, relative):
  ox=self.x;oy=self.oy
  if relative:
    self.x+=x
    self.y+=y
  for obj in self.parent.objects.get(object):
    if self == obj:continue
    if self.collidesWith(obj):
      self.x=ox;self.y=oy
      return True
  self.x=ox;self.y=oy
  return False