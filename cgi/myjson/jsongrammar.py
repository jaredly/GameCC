grammar = '''
<start> -> <value>
<value> -> <object> | <list> | <token>

<object> -> {<object contents>}
<object contents> -> <key>:<value><object tail> | <e>
<object tail> -> ,<object contents> | <e>
<key> -> <string> | <number> | <id>

<list> -> [<list contents>]
<list contents> -> <value><list tail> | <e>
<list tail> -> ,<list contents> | <e>

<token> -> <string> | <number> | <id>

<string> -> '<single contents>' | "<double contents>"
<single contents> -> \<char><single contents> | <not single><single contents> | <e>
<double contents> -> \<char><double contents> | <not double><double contents> | <e>
<no quotes> -> 0|1|2|3|4|5|6|7|8|9|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|!|#|$|%|&|(|)|*|+|,|-|.|/|:|;|=|?|@|[|\|]|^|_|`|{|}|~|<bar>|<lt>|<gt>|<space>|<tab>|<backn>|<backr>
<not single> -> <no quotes> | "
<not double> -> <no quotes> | '
<char> -> <no quotes> | " | '

<number> -> -<digit tail> | <digit tail>
<digit tail> -> <digit><digit rest> | .<digit><digits>
<digit rest> -> <digit tail> | <e>
<digits> -> <digit><digits> | <e>
<digit> -> 0|1|2|3|4|5|6|7|8|9

<id> -> <idstart><idtail>
<idtail> -> <idchar><idtail> | <e>
<idstart> -> a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|_
<idchar> -> <idstart>|0|1|2|3|4|5|6|7|8|9
'''

'''
  predefined tokens (b/c they are used in the lexer format...):
    <bar>   -> "|"
    <lt>    -> "<"
    <gt>    -> ">"
    <space> -> " "
    <tab>   -> "\t"
    <backr> -> "\r"
    <backn> -> "\n"
'''

