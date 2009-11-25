def output(data,type):
  if type=='haxe':
    return '''for (object in this.parent.objects.get(cast Type.resolveClass("%(object)s")).iterator()){
  if (object == this)continue;'''%data
  elif type=='python':
    return '''for object in self.parent.objects.get(%(object)s):
      if object == self:continue'''%data
