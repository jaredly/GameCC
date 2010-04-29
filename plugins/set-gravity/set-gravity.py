def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.setGravity(%(direction)s, %(speed)s);'%data
  elif type=='python':
    return '%(appliesto)s.setGravity(%(direction)s, %(speed)s);'%data
