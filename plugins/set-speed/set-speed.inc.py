def setSpeed(self, speed, speed_percent, relative):
  if speed_percent: self.speed *= speed
  elif relative: self.speed += speed
  else: self.speed = speed 
