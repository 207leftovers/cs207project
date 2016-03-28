import .ast as ast
from .error import *

class PrettyPrint(ast.ASTVisitor):
  def __init__(self):
    pass
  def visit(self, node):
    print(node.__class__.__name__)

class CheckSingleAssignment(ast.ASTVisitor):
  def __init__(self):
    self.component_names = []
    self.names_used = []

  def visit(self, node):
    #if the visitor visits a component, check if the name is taken. if it is not, initialize
    #an empty list for the component and insert into dictionary
    if isinstance(node, ast.ASTComponent):
      self.names_used = []
      new_component_name = node.name.name

      if new_component_name in self.component_names:
        raise PypeSyntaxError('Component name: ' + new_component_name +' has already been taken')
      else:
        self.component_names.append(new_component_name)
    elif isinstance(node, ast.ASTAssignmentExpr):
      name = node.binding.name
      if name in self.names_used:
        raise PypeSyntaxError('Node name: ' + name + '  has already been taken')
      else:
        self.names_used.append(name)
    elif isinstance(node, ast.ASTInputExpr):
      for input_expression in node.children:
        name = input_expression.name
        if name in self.names_used:
          raise PypeSyntaxError('Node name: ' + name + '  has already been taken')
        else:
          self.names_used.append(name)

class CheckSingleIOExpression(ast.ASTVisitor):
  def __init__(self):
    self.component = None
    self.component_has_input = False
    self.component_has_output = False

  def visit(self, node):
    if isinstance(node, ast.ASTComponent):
      self.component = node.name.name
      self.component_has_input = False
      self.component_has_output = False
    elif isinstance(node, ast.ASTInputExpr):
      if self.component_has_input:
        raise PypeSyntaxError('Component '+str(self.component)+' has multiple input expressions')
      self.component_has_input = True
    elif isinstance(node, ast.ASTOutputExpr):
      if self.component_has_output:
        raise PypeSyntaxError('Component '+str(self.component)+' has multiple output expressions')
      self.component_has_output = True

'''
class CheckUndefinedVariables(ast.ASTVisitor):
  def __init__(self, symtab):
    self.symtab = symtab
    self.scope=None

  def visit(self, node):
    if isinstance(node, ast.ASTComponent):
      self.scope = node.name.name
    elif isinstance(node, ast.ASTID):
      if self.symtab.lookupsym(node.name, scope=self.scope) is None:
        raise PypeSyntaxError('Undefined variable: '+str(node.name))
'''
