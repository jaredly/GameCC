def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.setV(%(direction)s,%(speed)s,%(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.setV(%(direction)s,%(speed)s,%(relative)s)'%data
