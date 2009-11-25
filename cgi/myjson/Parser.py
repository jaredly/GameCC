
import jsongrammar
import string

debug = False

def any(iterable):
  for i in iterable:
    if i:return True
  return False

def all(iterable):
  for i in iterable:
    if not i:return False
  return True

class Lexer:
  def __init__(self):
    self.data = []
    self.pos = 0
  def lex(self,data):
    self.data = data
    self.pos = 0
  def hasNextToken(self):
    return self.pos<len(self.data)
  def peek(self):
    if not self.hasNextToken():return '<eof>'
    return self.data[self.pos]
  def charline(self):
    return 0,0#len(self.data[:self.pos].split('\n')),len(self.data[:self.pos].split('\n')[-1])
  def nextToken(self):
    c = self.peek()
    self.advance()
    return c
  def advance(self):
    self.pos += 1
  def surrounds(self):
    return self.data[self.pos-10:self.pos+10]

def lexrule(x):
  convert = {'<bar>':'|','<lt>':'<','<gt>':'>','<space>':' ','<backr>':'\r','<backn>':'\n','<tab>':'\t'}
  parts = x.split('|')
  for part in parts:
    subs = []
    i = 0
    buff=''
    while i<len(part):
      buff = part[i]
      i+=1
      if buff=='<':
        while i<len(part) and part[i]!='>':
          buff+=part[i]
          i+=1
        if i<len(part):
          buff+=part[i]
          i+=1
        if i<len(part) and part[i]=='+':
          buff+=part[i]
          i+=1
        buff = buff.strip()
        if buff in convert:
          subs.append(convert[buff])
        else:
          subs.append(buff.strip())
        
      elif buff in ' \r\n\t':
        continue
      else:
        while i<len(part) and part[i] not in ' \r\n\t<>':
          buff+=part[i]
          i+=1
        subs.append(buff.strip())
    yield subs

class Rule:
  def __init__(self,parent,name,children):
    self.parent = parent
    self.name = name
    self.parentRule = None
    self.children = children
    self.tree = []
    self.value = None
  
  def __str__(self):
    if self.tree:
      return '<rule type="'+self.name+'" children="'+' '.join(x.name for x in self.tree)+'">'
    else:
      return '<rule type="'+self.name+'" value="'+self.value+'"/>'
  
  def reduce(self, names):
    if self.name in names:
      self.value = self.getvalue()
      self.tree = []
    else:
      [ch.reduce(names) for ch in self.tree]
  
  def output(self,ident=0):
    string = [ident/4*'.' + str(self)]
    for node in self.tree:
      string.append(node.output(ident+4))
    return '\n'.join(string)
  
  def getvalue(self):
    return ''.join(node.getvalue() for node in self.tree)
  
  def getNodesByTagName(self,name):
    ret = []
    if self.name==name:
      ret.append(self)
    for node in self.tree:
      ret += node.getNodesByTagName(name)
    return ret
  
  def clone(self):
    return Rule(self.parent,self.name,self.children)
  
  def hasFirst(self,token):
    return token in self.first()
  
  def remove(self):
    self.parentRule.removeChild(self)
  
  def removeChild(self, child):
    self.tree.remove(child)
  
  def first(self):
    res = []
    for child in self.children:
      if not child[0] in self.parent.rules:
        if not child[0].startswith('<'):
          res.append(child[0])
        else:
          raise Exception,'Child not found "%s"'%child[0]
      else:
        res += self.parent.rules[child[0]].first()
    return res
  
  def parse(self,lexer,depth=0):
    if self.parent.error:return
    if debug:print '.'*depth,'decending into',self.name,lexer.peek(),lexer.charline()
    nt = lexer.peek()
    tree = []
    
    while nt in ' \t\r\n':
      if not any(self.parent.rules[child[0]].hasFirst(nt) for child in self.children if not child[0]=='<e>'):
        #print 'skipping',[nt]
        lexer.advance()
        nt = lexer.peek()
      else:
        break

    
    for child in self.children: ## we will assume that it is LL(1)
      item = child[0]
      if item.endswith('>+'):item=item[:-1]
      if self.parent.rules[item].hasFirst(nt):
        break
    else:
      self.parent.error = 'Syntax Error: "%s" should be a %s at line,char %s (near %s)'%(nt,self.name,lexer.charline(),lexer.surrounds())
      return
    
    for item in child:
      if self.parent.error:return
      rep = False
      if item.endswith('>+'):
        rep = True
        item = item[:-1]
      rule = self.parent.rules[item].clone()
      rule.parentRule = self
      rule.parse(lexer,depth+1)
      tree.append(rule)
      if rep:
        while self.parent.rules[item].hasFirst(lexer.peek()):
          #print 'repeat',lexer.peek(),item
          if self.parent.error:return
          rule = self.parent.rules[item].clone()
          rule.parentRule = self
          rule.parse(lexer,depth+1)
          tree.append(rule)
    
    self.tree = tree
    if debug:print ' '*depth,'done w/',self.name

class LexRule(Rule):
  def __init__(self,parent,name):
    self.parent = parent
    self.parentRule = None
    self.name = name
    self.children = []
    self.tree = []
    self.value = ''
  
  def __str__(self):
    return '<Rule type="'+self.name+'">'
  
  def getvalue(self):
    return self.value
  
  def clone(self):
    return LexRule(self.parent,self.name)
  
  def first(self):
    return [self.name]
  
  def hasFirst(self,token):
    return token==self.name
  
  def parse(self,lexer,depth=0):
    if lexer.peek() in ' \t\r\n' and not self.name in ' \t\r\n':
      lexer.advance()
    if lexer.peek() == self.name:
      self.value = lexer.nextToken()
      if debug:print ' '*depth,'got',self.value
      return True
    else:
      self.parent.error = 'Syntax Error: "%s" should be "%s" while parsing a "%s" at line, char %s (near %s)'%(lexer.peek(),self.name,self.parentRule.name,lexer.charline(),lexer.surrounds())
      #print
      #sys.exit()#raise Exception,'this shouldn\'t happen -- invalid lex tree "%s" should be "%s"'%(lexer.peek(),self.name)

class EmptyRule(LexRule):
  def first(self):
    return []
  
  def clone(self):
    return EmptyRule(self.parent,self.name)
  
  def hasFirst(self,token):
    return True
  
  def parse(self,lexer,depth=0):
    return ''

class EOFRule(EmptyRule):
  pass

class Parser:
  grammar = jsongrammar.grammar
  start = '<start>'
  def __init__(self,filename):
    if hasattr(filename,'read'):
      filename = filename.read()
    self.filedata = filename
    self.lexer = Lexer()
    self.rules = {'<e>':EmptyRule(self,'<e>'),'<eof>':EOFRule(self,'')}
    self.loadGrammar()
    #print self.rules.keys()
    self.lexer.lex(list(filename.strip()))
    self.error = False
    
    #self.tokenize()
    
    if self.error:
      raise Exception,self.error
    
    global debug
    debug = False
    self.start = '<start>'
    self.parse()
    
    if self.error:
      raise Exception,self.error
    if self.lexer.hasNextToken():
      print self.filedata
      print [self.lexer.peek()]
      raise Exception,'extra end chars'
    
    #print self.base.getvalue()

  def loadGrammar(self):
    text = self.grammar
    lines = text.split('\n')
    rules = dict([a.strip() for a in x.split('->')] for x in lines if x)
    for rule in rules:
      self.rules[rule] = Rule(self,rule,list(lexrule(rules[rule])))
    
    for a in string.printable:
      self.addLexRule(a)
    
    for name,rule in self.rules.items():
      for sub in rule.children:
        for child in sub:
          if not (child.startswith('<') and (child.endswith('>') or child.endswith('>+'))):
            self.addLexRule(child)
    
  def addLexRule(self,ttype):
    ntype = ttype
    self.rules[ntype] = LexRule(self,ttype)
  
  def parse(self):
    self.base = self.rules[self.start].clone()
    self.base.parse(self.lexer)
  
  def tokenize(self):
    base = self.rules['<tokens>'].clone()
    base.parse(self.lexer)
    tokens = base.getNodesByTagName('<token>')
    if self.lexer.hasNextToken():
      print [self.lexer.peek()]
      raise Exception,'extra end chars'
    
    self.lexer.lex([t.getvalue() for t in tokens])
  
  def __str__(self):
    return ''#self.base.output()

def test(x):
  return Parser(x).base.getvalue()

if __name__=='__main__':
  import sys
  if not len(sys.argv)>1:
    print 'Usage: python Parser.py input_file'
    sys.exit(0)
  print Parser(open(sys.argv[1]))
