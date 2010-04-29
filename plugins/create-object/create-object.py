def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.createObject("%(object)s", %(x)s, %(y)s, %(relative)s, %(direction)s, %(speed)s);'%data
  elif type=='python':
    return '%(appliesto)s.createObject("%(object)s", %(x)s, %(y)s, %(relative)s, %(direction)s, %(speed)s);'%data
