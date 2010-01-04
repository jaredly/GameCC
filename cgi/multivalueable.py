
class ArgumentError(Exception):
  pass

def clean(x):
  return x.replace('\\','\\\\').replace("'","\\'")

types = 'number', 'select', 'select string', 'object', 'direction', 'percent', 'key', 'bool', 'check', 'random', 'randint', 'variable', 'timer', 'custom', 'string'

keys = {
  'haxe': {8: 'backspace', 9: 'tab', 13: 'enter', 16: 'shift', 17: 'control', 19: 'pause_break', 20: 'caps_lock', 27: 'esc', 32: 'spacebar', 33: 'page_up', 34: 'page_down', 35: 'end', 36: 'home', 37: 'left_arrow', 38: 'up_arrow', 39: 'right_arrow', 40: 'down_arrow', 45: 'insert', 46: 'delete', 48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e', 70: 'f', 71: 'g', 72: 'h', 73: 'i', 74: 'j', 75: 'k', 76: 'l', 77: 'm', 78: 'n', 79: 'o', 80: 'p', 81: 'q', 82: 'r', 83: 's', 84: 't', 85: 'u', 86: 'v', 87: 'w', 88: 'x', 89: 'y', 90: 'z', 96: 'numpad_0', 97: 'numpad_1', 98: 'numpad_2', 99: 'numpad_3', 100: 'numpad_4', 101: 'numpad_5', 102: 'numpad_6', 103: 'numpad_7', 104: 'numpad_8', 105: 'numpad_9', 106: 'multiply', 107: 'add', 109: 'subtract', 110: 'decimal', 111: 'divide', 112: 'f1', 113: 'f2', 114: 'f3', 115: 'f4', 116: 'f5', 117: 'f6', 118: 'f7', 119: 'f8', 120: 'f9', 122: 'f11', 123: 'f12', 124: 'f13', 125: 'f14', 126: 'f15', 144: 'num_lock', 145: 'scrlk'},
  'python': {'K_KP_MINUS': 'keypad minus', 'K_F1': 'F1', 'K_F2': 'F2', 'K_PAUSE': 'pause', 'K_COLON': 'colon', 'K_F5': 'F5', 'K_F6': 'F6', 'K_F7': 'F7', 'K_F8': 'F8', 'K_F9': 'F9', 'K_COMMA': 'comma', 'K_F3': 'F3', 'K_F4': 'F4', 'K_AMPERSAND': 'ampersand', 'K_CLEAR': 'clear', 'K_KP_PLUS': 'keypad plus', 'K_KP_EQUALS': 'keypad equals', 'K_LEFT': 'left arrow', 'K_INSERT': 'insert', 'K_HOME': 'home', 'K_LSUPER': 'left windows key', 'K_GREATER': 'greater-than sign', 'K_RALT': 'right alt', 'K_KP_PERIOD': 'keypad period', 'K_BREAK': 'break', 'K_RIGHTBRACKET': 'right bracket', 'K_RSHIFT': 'right shift', 'K_LSHIFT': 'left shift', 'K_LEFTPAREN': 'left parenthesis', 'K_DOLLAR': 'dollar', 'K_KP_ENTER': 'keypad enter', 'K_PAGEDOWN': 'page down', 'K_HASH': 'hash', 'K_DOWN': 'down arrow', 'K_END': 'end', 'K_UP': 'up arrow', 'K_ASTERISK': 'asterisk', 'K_LCTRL': 'left ctrl', 'K_BACKSLASH': 'backslash', 'K_MINUS': 'minus sign', 'K_RSUPER': 'right windows key', 'K_EXCLAIM': 'exclaim', 'K_HELP': 'help', 'K_POWER': 'power', 'K_ESCAPE': 'escape', 'K_BACKSPACE': 'backspace', 'K_MENU': 'menu', 'K_UNDERSCORE': 'underscore', 'K_QUOTEDBL': 'quotedbl', 'K_KP_MULTIPLY': 'keypad multiply', 'K_LEFTBRACKET': 'left bracket', 'K_LALT': 'left alt', 'K_KP_DIVIDE': 'keypad divide', 'K_NUMLOCK': 'numlock', 'K_RMETA': 'right meta', 'K_SPACE': 'spacebar', 'K_RIGHT': 'right arrow', 'K_EQUALS': 'equals sign', 'K_SYSREQ': 'sysrq', 'K_SEMICOLON': 'semicolon', 'K_QUESTION': 'question mark', 'K_EURO': 'euro', 'K_PERIOD': 'period', 'K_DELETE': 'delete', 'K_CARET': 'caret', 'K_LMETA': 'left meta', 'K_TAB': 'tab', 'K_MODE': 'mode shift', 'K_SLASH': 'forward slash', 'K_F12': 'F12', 'K_F13': 'F13', 'K_F10': 'F10', 'K_F11': 'F11', 'K_F14': 'F14', 'K_F15': 'F15', 'K_y': 'y', 'K_x': 'x', 'K_z': 'z', 'K_q': 'q', 'K_p': 'p', 'K_s': 's', 'K_r': 'r', 'K_u': 'u', 'K_t': 't', 'K_w': 'w', 'K_v': 'v', 'K_i': 'i', 'K_h': 'h', 'K_k': 'k', 'K_j': 'j', 'K_m': 'm', 'K_l': 'l', 'K_o': 'o', 'K_n': 'n', 'K_a': 'a', 'K_c': 'c', 'K_b': 'b', 'K_e': 'e', 'K_d': 'd', 'K_g': 'g', 'K_f': 'f', 'K_AT': 'at', 'K_PAGEUP': 'page up', 'K_CAPSLOCK': 'capslock', 'K_LESS': 'less-than sign', 'K_PRINT': 'print screen', 'K_RETURN': 'return', 'K_SCROLLOCK': 'scrollock', 'K_9': '9', 'K_8': '8', 'K_1': '1', 'K_0': '0', 'K_3': '3', 'K_2': '2', 'K_5': '5', 'K_4': '4', 'K_7': '7', 'K_6': '6', 'K_PLUS': 'plus sign', 'K_BACKQUOTE': 'grave', 'K_QUOTE': 'quote', 'K_RIGHTPAREN': 'right parenthesis', 'K_RCTRL': 'right ctrl', 'K_KP8': 'keypad 8', 'K_KP9': 'keypad 9', 'K_KP4': 'keypad 4', 'K_KP5': 'keypad 5', 'K_KP6': 'keypad 6', 'K_KP7': 'keypad 7', 'K_KP0': 'keypad 0', 'K_KP1': 'keypad 1', 'K_KP2': 'keypad 2', 'K_KP3': 'keypad 3'}
}

reversed_keys = {}
for otype,dct in keys.items():
  reversed_keys[otype] = dict((v.replace(' ','_').replace('/','_'),k) for k,v in dct.items())

## reversekey = dict((v,k) for k,v in keynames.items())
## reversecodes = dict((v.replace(' ','_').replace('/','_'),k) for k,v in pycodes.items())

_string = lambda data,otype,c:"'%s'"%clean(data)
_plain  = lambda data,otype,c:data

true = {'python':'True','haxe':'true'}
false = {'python':'False','haxe':'false'}
bools = [false, true]

def _convert_number(data,otype,c):
  if float(data) == int(data):
    return str(int(data))
  return str(float(data))

def _convert_object(data,otype,c):
  if data not in c.parent.assets['objects']:
    raise ArgumentError, 'convert object %s'%data
  return data

def _convert_random(data,otype,c):
#  print data,len(data)
  if otype == 'haxe':
    return 'Random.randrange(%s,%s)'%tuple(data)
  elif otype == 'python':
    return 'random.randrange(%s,%s)'%tuple(data)

def _convert_randint(data,otype,c):
  if otype == 'haxe':
    return 'Std.int(Random.randrange(%s,%s))'%tuple(data)
  elif otype == 'python':
    return 'int(random.randrange(%s,%s))'%tuple(data)

def _convert_variable(data,otype,c):
  if data[0] == 'game':
    data[0] = 'self'
    data[1] = 'parent.'+data[1]
  selfs = {'python':'self','haxe':'this'}
  if data[0] == 'self':data[0] = selfs[otype]
  return '%s.%s'%tuple(data)

def _convert_not(data,otype,c):
  if data:
    return {'python':'not ','haxe':'!'}[otype]
  else:
    return ''

convert = {
  'number':_convert_number,
  'select':_plain,
  'select string':_string,
  'object':_convert_object,
  'direction':_convert_number,
  'percent':(lambda data,otype,c:'.%s'%data),
  'key':(lambda data,otype,c:reversed_keys[otype][data]),
  'bool':(lambda data,otype,c:bools[data][otype]),
  'not':_convert_not,
  'random':_convert_random,
  'randint':_convert_randint,
  'variable':_convert_variable,
  'timer':_convert_number,
  'custom':_plain,
}


