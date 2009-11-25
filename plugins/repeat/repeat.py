def output(data,type):
  if type=='haxe':
    return 'for (i in 0...%(num)s){'%data
  elif type=='python':
    return 'for i in range(%(num)s):'%data
