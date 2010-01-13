def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.setVspeed(%(speed)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.setVspeed(%(speed)s, %(relative)s);'%data
