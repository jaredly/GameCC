def output(data,type):
  if type=='haxe':
    return '%(appliesto)s.wrapPositionToScreen("%(vhb)s");'%data
  elif type=='python':
    return '%(appliesto)s.wrapPositionToScreen("%(vhb)s")'%data
