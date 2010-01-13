def output(data,type):
  if type=='haxe':
    return '%(not)s(Random.randrange(0,%(odds)s)==0)'%data
  elif type=='python':
    return '%(not)s(random.randrange(0,%(odds)s)==0)'%data
