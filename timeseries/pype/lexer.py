import ply.lex

reserved = { # pattern : token-name
  'input' : 'INPUT',
  'output' : 'OUTPUT',
  'import' : 'IMPORT',
}
# 'tokens' is a special word in ply's lexers.
tokens = [ 
  'LPAREN','RPAREN', # Individual parentheses
  'LBRACE','RBRACE', # Individual braces
  'OP_ADD','OP_SUB','OP_MUL','OP_DIV', # the four basic arithmetic symbols
  'STRING', # Anything enclosed by double quotes
  'ASSIGN', # The two characters :=
  'NUMBER', # An arbitrary number of digits
  'ID', # a sequence of letters, numbers, and underscores. Must not start with a number.
] + list(reserved.values())

# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\['
t_RBRACE  = r'\]'
t_ADD    = r'\+'
t_SUB   = r'-'
t_MUL   = r'\*'
t_DIV  = r'/'

t_STRING = r'"[^"]"'
    
t_ASSIGN = r':='

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Ignore whitespace (spaces and tabs)
t_ignore = ' \t'

# Write one rule for IDs and reserved keywords. Section 4.3 has an example.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignore comments. Comments in PyPE are just like in Python. Section 4.5.
t_ignore_COMMENT = r'\#.*'

# Write a rule for newlines that track line numbers. Section 4.6.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Write an error-handling routine. It should print both line and column numbers.
def t_error(t):
    print("Illegal character '%s', line %d, column %d" % (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)

# This actually builds the lexer.
lexer = ply.lex.lex(debug=True)