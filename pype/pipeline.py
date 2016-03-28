from .lexer import lexer
from .parser import parser
from .ast import *
from .semantic_analysis import CheckSingleAssignment, CheckSingleIOExpression, PrettyPrint#, CheckUndefinedVariables
from .translate import SymbolTableVisitor

class Pipeline(object):
  def __init__(self, source):
    with open(source) as f:
      self.compile(f)

  def compile(self, file):
    input = file.read()

    # Lexing, parsing, AST construction
    ast = parser.parse(input, lexer=lexer)
    
    # Semantic analysis
    ast.walk( CheckSingleAssignment() )
    ast.walk( CheckSingleIOExpression() )
    #ast.walk( CheckUndefinedVariables(syms) )
    
    # Translation
    syms = ast.walk( SymbolTableVisitor() )
    
    # Pretty print
    # ast.pprint()
    # ast.walk(PrettyPrint())
    syms.pprint()

    return syms