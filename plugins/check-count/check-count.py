def output(data,type):
  if type=='haxe':
    return '%(not)s(this.parent.objects.get(%(object)s).length %(operator)s %(number)s)'%data
  elif type=='python':
    return '%(not)s(self.parent.objects.get(%(object)s) %(operator)s %(number)s)'%data
