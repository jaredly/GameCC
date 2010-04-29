def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.gravityTowards(%(x)s, %(y)s, %(gravity)s, %(relative)s);'%data
  elif type=='python':
    return '%(appliesto)s.gravityTowards(%(x)s, %(y)s, %(gravity)s, %(relative)s);'%data
