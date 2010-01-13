def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.moveTowards(%(x)s, %(y)s, %(amount)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.moveTowards(%(x)s, %(y)s, %(amount)s, %(relative)s);'%data
