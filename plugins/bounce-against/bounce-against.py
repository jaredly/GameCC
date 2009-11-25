def output(data,type):
  if type=='haxe':
    return 'this.bounceAgainst(other);'%data
  elif type=='python':
    return 'self.bounceAgainst(other)'%data
