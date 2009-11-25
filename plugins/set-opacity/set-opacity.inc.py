def setOpacity(self, opacity, opacity_percent, relative):
  if opacity_percent:self.opacity *= opacity
  elif relative:self.opacity += opacity
  else:self.opacity = opacity
