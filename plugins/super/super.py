def output(data,type):
  if type=='haxe':
    return 'super.%(_event)s(%(_args)s);'%data
  elif type=='python':
    return '%(_parent)s.%(_event)s(self,%(_args)s);'%data
