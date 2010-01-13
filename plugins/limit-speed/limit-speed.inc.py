def limitSpeed(self,speed):
  if self.speed > speed:self.speed = speed
  if self.speed < -speed:self.speed = -speed
