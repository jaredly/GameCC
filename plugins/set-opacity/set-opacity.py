def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.setOpacity(%(opacity)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.setOpacity(%(opacity)s, %(relative)s);'%data
