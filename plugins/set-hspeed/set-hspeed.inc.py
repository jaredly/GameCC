def setHspeed(self, speed, speed_percent, relative):
  if speed_percent:
    self.hspeed *= speed
  elif relative:
    self.hspeed += speed
  else:
    self.hspeed = speed
