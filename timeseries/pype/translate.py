import ast
#from .ast import *
from .symtab import *
from .lib_import import LibraryImporter

class SymbolTableVisitor(ast.ASTVisitor):
  def __init__(self):
    self.symbol_table = SymbolTable()
    self.currentComponent = None

  def return_value(self):
    return self.symbol_table

  def visit(self, node):
    if isinstance(node, ast.ASTImport):
      # Import statements make library functions available to PyPE
      imp = LibraryImporter(node.module.name)
      #print(imp)
      print('ANOVE')
      print (imp.add_symbols(self.symbol_table))
      print('Below')

    # TODO
    # Add symbols for the following types of names:
    #   inputs: anything in an input expression
    #     the SymbolType should be input, and the ref can be None
    #     the scope should be the enclosing component
    #   assigned names: the bound name in an assignment expression
    #     the SymbolType should be var, and the ref can be None
    #     the scope should be the enclosing component
    #   components: the name of each component
    #     the SymbolType should be component, and the ref can be None
    #     the scope sould be *global*
    
    # Note, you'll need to track scopes again for some of these.
    # You may need to add class state to handle this.
    
    if isinstance(node, ast.ASTInputExpr):
      for input_expression in node.children:
        name = input_expression.name
        self.symbol_table.addsym((name, SymbolType.input, None), self.currentComponent)
    elif isinstance(node, ast.ASTAssignmentExpr):
      name = node.binding.name
      self.symbol_table.addsym((name, SymbolType.var, None), self.currentComponent)
    elif isinstance(node, ast.ASTComponent):
      name = node.name.name
      self.currentComponent = name
      self.symbol_table.addsym((name, SymbolType.component, None), 'global')
    
