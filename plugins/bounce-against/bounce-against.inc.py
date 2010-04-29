def bounceAgainst(object):
  v = self.velocity.clone()
  v.magnitude = -self.velocity.magnitude/10.0
  for i in range(10):
    if not self.collidesWith(object):break
    self.x += v.x()
    self.y += v.y()
  a = self.angle_to(object.x,object.y)
  a/= math.pi/2
  a = int(a) * math.pi/2
  self.velocity.bounce_off(a+math.pi/2)
