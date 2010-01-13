def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.setDirection(%(direction)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.setDirection(%(direction)s, %(relative)s);'%data
