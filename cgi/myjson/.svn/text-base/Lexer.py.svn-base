import string

class Reader:
  def __init__(self,string):
    self.data = string
    self.lineno = 1
    self.pos = 0
  def hasNextChar(self):
    return self.pos<len(self.data)
  def nextChar(self):
    char = self.data[self.pos]
    self.advance()
    return char
  def peek(self):
    return self.data[self.pos]
  def advance(self):
    if self.peek()=='\n':
      self.lineno += 1
    self.pos += 1

class Token:
  def __init__(self,ttype,value,lineno):
    self.type = ttype
    self.value = value
    self.lineno = lineno
  def __str__(self):
    return '(%s,"%s",%d)'%(self.type,self.value,self.lineno)

class Lexer:
  symbols = {':':'COLON',
             ',':'COMMA',
             '{':'LEFT_CURL',
             '}':'RIGHT_CURL',
             '[':'LEFT_SQUARE',
             ']':'RIGHT_SQUARE',
             '(':'LEFT_PAREN',
             ')':'RIGHT_PAREN',
             '.':'PERIOD'}
  def __init__(self):
    self.allowed = self.symbols.values()
    self.allowed += ['STRING','COMMENT','EOF', 'ID', 'NUMBER', 'TRUE', 'FALSE', 'NULL']
    self.start_symbols = set(s[0] for s in self.symbols)
    self.tpos = 0
  
  def __str__(self):
    return '\n'.join(str(t) for t in self.tokens)+'\nTotal Tokens: = %d'%len(self.tokens)
  
  def peek(self):
    #print 'getting token',self.tokens[self.tpos]
    return self.tokens[self.tpos]
  
  def advance(self):
    self.tpos += 1
  
  def nextToken(self):
    res = self.peek()
    self.advance()
    return res
  
  def hasNextToken(self):
    return self.tpos < len(self.tokens)
  
  def lex(self, data):
    self.buff = Reader(data)
    self.tokens = []
    self.startline = self.buff.lineno
    
    while self.buff.hasNextChar():
      current = self.buff.peek()
      if current in string.ascii_letters:
        self.getIdentifier()
      elif current in string.digits+'-':
        self.getNumber()
      elif current == "'" or current == '"':
        self.getString()
      elif current in self.start_symbols:
        self.getSymbol()
      elif current in ' \r\n':
        self.buff.advance()
        if current == '\n':
          self.startline = self.buff.lineno
      else:
        self.addToken('UNDEFINED',current)
        self.buff.advance()
      self.startline = self.buff.lineno
    if len(self.tokens):
      self.buff.lineno += 1
    self.startline = self.buff.lineno
    self.addToken('EOF',"")
      
  def getIdentifier(self):
    buff = self.buff.nextChar()
    while self.buff.hasNextChar() and self.buff.peek() in string.ascii_letters+string.digits+'_':
      buff += self.buff.nextChar()
    if buff == 'false':
      self.addToken('FALSE',buff)
    elif buff == 'true':
      self.addToken('TRUE',buff)
    elif buff == 'null':
      self.addToken('NULL',buff)
    else:
      self.addToken('ID',buff);
  
  def getNumber(self):
    buff = self.buff.nextChar()
    while self.buff.hasNextChar() and self.buff.peek() in string.digits+'.':
      buff += self.buff.nextChar()
    self.addToken('NUMBER',buff);
  
  def getString(self):
    buff = self.buff.nextChar()
    while self.buff.hasNextChar():
      if self.buff.peek()=="\\":
        buff += self.buff.nextChar()
      elif self.buff.peek()==buff[0]:
        buff += self.buff.nextChar()
        break
      buff += self.buff.nextChar()
    else:
      return self.addToken('UNDEFINED',buff)
    self.addToken('STRING', buff[1:-1])
    
  def getSymbol(self):
    buff = self.buff.nextChar()
    while self.buff.hasNextChar():
      if self.checkSymbol(buff + self.buff.peek()):
        buff += self.buff.nextChar()
      else:
        break
    for x in self.symbols:
      if x==buff:
        return self.addToken(self.symbols[x],buff)
    self.addToken('UNDEFINED',buff)

  def checkSymbol(self,x):
    for s in self.symbols:
      if s.startswith(x):
        return True

  def addToken(self, ttype, string):
    if ttype not in self.allowed:
      raise Exception,'invalid token type "%s" with value "%s"'%(ttype,string)
    #print 'token',ttype,[string]
    self.tokens.append(Token(ttype,string,self.startline))

if __name__=='__main__':
  l = Lexer()
  l.lex(open('../../projects/Project3/maps/Maps1.info').read().replace('"',"'"))
  print l
