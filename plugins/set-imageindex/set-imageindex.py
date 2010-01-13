def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.imagepos = %(index)s;'%data
  elif type=='python':
    return '%(appliesto)s.imagepos = %(index)s;'%data
