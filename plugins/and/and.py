def output(data,type):
  if type=='haxe':
    return 'if (%(a)s && %(b)s){'%data
  elif type=='python':
    return 'if %(a)s and %(b)s:'%data
