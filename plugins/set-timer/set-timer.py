def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.setTimer(%(timer)s, %(amount)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.setTimer(%(timer)s, %(amount)s, %(relative)s);'%data
