import Parser
import jsongrammar

class JsonParser(Parser.Parser):
  grammar = jsongrammar.grammar
  start = '<json>'
  def toObject(self, item = None):
    if not item:
      item = self.base

    predefs = {'true':True,'false':False,'null':None}
    if item.name == '<id>':
      v = item.getvalue()
      if not v in predefs:
        raise Exception,v
      v = predefs.get(v)
      return v
    elif item.name == '<string>':
      return item.getvalue()[1:-1];
    elif item.name == '<number>':
      v = item.getvalue()
      if '.' in v:
        return float(v)
      return int(v)

      return item.getvalue()

    ignore = list('{}[],:')+['<e>']
    tree = [x for x in item.tree if not x.name in ignore]

    if item.name == '<list>':
      ret = []
      tail = self.toObject(tree[0])
      if tail:
        ret += tail
      return ret
    if item.name == '<object>':
      ret = {}
      tail = self.toObject(tree[0])
      if tail:
        ret.update(tail)
      return ret


    if item.name == '<list contents>':
      if not len(tree):return []
      ret = [self.toObject(tree[0])]
      tail = self.toObject(tree[1])
      if tail:
        ret += tail
      return ret
    elif item.name == '<object contents>':
      if not len(tree):return {}
      ret = {self.toObject(tree[0]):self.toObject(tree[1])}
      tail = self.toObject(tree[2])
      if tail:
        ret.update(tail)
      return ret

    if len(tree)==1:
      return self.toObject(tree[0])
    elif not len(tree):
      if item.name == '<object>':
        return {}
      elif item.name == '<list>':
        return []
      #else:
      #  print tree,item
      #  raise Exception,"badness"
    else:
      print tree,item
      raise Exception,"badness"

def load(x):
  return JsonParser(x).toObject()

def loads(x):
  if not x:return None
  return JsonParser(x).toObject()

def dumps(x):
  return jsonify(x)

def jsonify(obj):
  if type(obj) in (str,unicode):
    return "'"+obj.replace("'","\\'").replace('\n','\\n')+"'"
  elif type(obj) in (int,float):
    return str(obj)
  elif type(obj) == long:
    return str(obj).strip('L')
  elif type(obj) == bool:
    return str(obj).lower()
  elif type(obj) in (list,tuple):
    return '[' + ', '.join(jsonify(elem) for elem in obj) + ']'
  elif type(obj) == dict:
    return '{ ' + ', '.join(jsonify(k)+':'+jsonify(v) for k,v in obj.items()) + ' }'
  elif obj is None:
    return 'null'
  raise Exception,"item can't be jsonified '%s' - of type %s"%(obj,type(obj))

def dump(x, where):
  where.write(jsonify(x))


if __name__=='__main__':
  print JsonParser(open('../../projects/Project3/maps/Maps1.info').read()).toObject()
