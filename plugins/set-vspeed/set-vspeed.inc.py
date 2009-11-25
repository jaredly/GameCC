def setVspeed(self, speed, speed_percent, relative):
  if speed_percent:self.vspeed *= speed
  elif relative:self.vspeed += speed
  else:self.vspeed = speed
