def output(data,type):
  if type=='haxe':
    return 'this.parent.remove(%(appliesto)s);'%data
  elif type=='python':
    return 'self.parent.remove(%(appliesto)s);'%data
