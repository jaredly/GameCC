def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.moveTo(%(x)s, %(y)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.moveTo(%(x)s, %(y)s, %(relative)s);'%data
