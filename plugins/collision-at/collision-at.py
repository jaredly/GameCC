def output(data,type):
  if type=='haxe':
    return '%(not)s%(appliesto)s.collisionAt(%(x)s, %(y)s, "%(object)s", %(relative)s)'%data
  elif type=='python':
    return '%(not)s%(appliesto)s.collisionAt(%(x)s, %(y)s, %(object)s, %(relative)s)'%data
