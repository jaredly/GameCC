def setV(self,direction, speed, rel):
  if rel:
    self._velocity += Vector(direction, speed)
  else:
    self._velocity = Vector(direction, speed)
