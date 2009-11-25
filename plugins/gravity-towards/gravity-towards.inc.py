def gravityTowards(self,x, y, gravity, relative):
  v = Vector.frompos(x-self.x,y-self.y)
  v.magnitude = gravity
  if relative:
    self._gravity += v
  else:
    self._gravity = v
