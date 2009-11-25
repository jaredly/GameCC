def output(data,type):
  if type=='haxe':
    return 'this.keepOnScreen(%(bounce)s);'%data
  elif type=='python':
    return '%(appliesto)s.keepOnScreen(%(bounce)s);'%data
