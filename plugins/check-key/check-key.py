def output(data,type):
  if type=='haxe':
    return '%(not)sthis.parent.keys[%(key)s]'%data
  elif type=='python':
    return '%(not)sself.parent.keys()[%(key)s]'%data
