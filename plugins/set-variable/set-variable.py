def output(data,type):
  if type=='haxe':
    return '%(variable)s = %(value)s;'%data
  elif type=='python':
    return '%(variable)s = %(value)s'%data
