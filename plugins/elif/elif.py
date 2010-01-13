def output(data,type):
  if type=='haxe':
    return '} else if (%(cond)s){'%data
  elif type=='python':
    return 'elif %(cond)s:'%data
