def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.moveToCollision(%(direction)s, %(amount)s, "%(object)s");'%data
  elif type=='python':
    return '%(appliesto)s.moveToCollision(%(direction)s, %(amount)s, %(object)s);'%data
