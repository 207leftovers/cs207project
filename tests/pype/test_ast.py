from pype import lexer
from pype import parser
from pype import ast
from pype.translate import SymbolTableVisitor
from pype.symtab import *
from pype.semantic_analysis import ASTVisitor

class PrettyString(ASTVisitor):
  def __init__(self):
    self.text = ''
  def visit(self, node):
    self.text += (node.__class__.__name__)

def test_basic_ast():
    input = "{sum (a + b)}"
    ast = parser.parse(input, lexer=lexer)
    syms = ast.walk(SymbolTableVisitor())
    assert syms['global'] == {'sum': Symbol(name='sum', type=SymbolType.component, ref=None)}
    
def test_input_ast():
    input = "{(INPUT xs)}"
    ast = parser.parse(input, lexer=lexer)
    pretty = PrettyString()
    ast.walk(pretty)
    print(pretty.text)
    assert pretty.text == 'ASTProgramASTComponentASTIDASTID'