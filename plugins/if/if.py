def output(data,type):
  if type=='python':
    return 'if %(expression)s:'%data
  elif type=='haxe':
    return 'if (%(expression)s){'%data
