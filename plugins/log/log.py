def output(data,type):
  if type=='haxe':
    return 'trace(%(log)s);'%data
  elif type=='python':
    return 'self.parent.log(%(log)s)'%data
