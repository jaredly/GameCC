def output(data,type):
  if type=='haxe':
    return '%(not)s(%(var1)s %(op)s %(var2)s)'%data
  elif type=='python':
    return '%(not)s(%(var1)s %(op)s %(var2)s)'%data
