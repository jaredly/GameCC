def moveToCollision(self, direction, amount, object):
  v = Vector(direction, amount)
  amt = 10.0
  if v.magnitude>10:amt = float(int(v.magnitude/2))
  v.magnitude/=amt
  if self.collisionAt(0, 0, object, True):
    for i in range(amt):
      self.moveTo(-v.x, -v.y, True)
      if not self.collisionAt(0, 0, object, True):
        return
  else:
    for i in range(amt):
      self.moveTo(v.x, v.y, True)
      if self.collisionAt(0, 0, object, True):
        self.moveTo(-v.x, -v.y, True)
        return
