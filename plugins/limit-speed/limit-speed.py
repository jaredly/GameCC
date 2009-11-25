def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.limitSpeed(%(speed)s);'%data
  elif type=='python':
    return '%(appliesto)s.limitSpeed(%(speed)s);'%data
