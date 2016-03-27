from .lexer import lexer
import parser
from .ast import *
#from .semantic_analysis import CheckSingleAssignment
#from .translate import SymbolTableVisitor

class Pipeline(object):
  def __init__(self, source):
    with open(source) as f:
      self.compile(f)

  def compile(self, file):
    input = file.read()
    print(input)
    # Lexing, parsing, AST construction
    ast = parser.parser.parse(input, lexer=lexer)
    print(ast)
    # Semantic analysis
    #ast.walk( CheckSingleAssignment() )
    # Pretty print
    ast.pprint()
    
    # Translation
    #syms = ast.walk( SymbolTableVisitor() )
    #return syms
