def moveTowards(self, x, y, amount, amount_percent, relative):
  if relative:
    x+=self.x;y+=self.y
  nv = Vector.frompos(x-self.x,y-self.y)
  if amount_percent:nv.magnitude *= amount
  else:nv.magnitude = amount
  self.x += nv.x
  self.y += nv.y
