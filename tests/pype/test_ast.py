from pype import lexer
from pype import parser
from pype import ast
from pype.translate import SymbolTableVisitor
from pype.symtab import *

def test_ast():
    input = "{sum (a + b)}"
    ast = parser.parse(input, lexer=lexer)
    syms = ast.walk(SymbolTableVisitor())
    assert syms['global'] == {'sum': Symbol(name='sum', type=SymbolType.component, ref=None)}