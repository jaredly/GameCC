def setImageRotation(self, rotation, relative):
  if relative:self.rotation += rotation
  else:self.rotation = rotation
