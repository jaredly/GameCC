def output(data,type):
  if type=='haxe':
    return 'this.imagespeed = %(speed)s;'%data
  elif type=='python':
    return 'self.imagespeed = %(speed)s;'%data
