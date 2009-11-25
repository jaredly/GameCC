def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.setImageRotation(%(rotation)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.setImageRotation(%(rotation)s, %(relative)s);'%data
