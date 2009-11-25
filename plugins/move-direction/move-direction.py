def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.moveDirection(%(direction)s, %(speed)s);'%data
  elif type=='python':
    return '%(appliesto)s.moveDirection(%(direction)s, %(speed)s);'%data
