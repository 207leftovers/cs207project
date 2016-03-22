
class ASTVisitor():
  def visit(self, astnode):
    'A read-only function which looks at a single AST node.'
    pass
  def return_value(self):
    return None

class ASTNode(object):
  def __init__(self):
    self.parent = None
    self._children = []

  @property
  def children(self):
    return self._children
  @children.setter
  def children(self, children):
    self._children = children
    for child in children:
      child.parent = self

  def pprint(self,indent=''):
    '''Recursively prints a formatted string representation of the AST.'''
    # TODO-check
    print self.parent
    for child in self._children:
      child.pprint(indent)

  def walk(self, visitor):
    '''Traverses an AST, calling visitor.visit() on every node.

    This is a depth-first, pre-order traversal. Parents will be visited before
    any children, children will be visited in order, and (by extension) a node's
    children will all be visited before its siblings.
    The visitor may modify attributes, but may not add or delete nodes.'''
    # TODO-check
    visitor.visit()
    for child in self.children:
      child.walk(visitor)

    return visitor.return_value()

class ASTProgram(ASTNode):
  def __init__(self, statements):
    super().__init__()
    self.children = statements

class ASTImport(ASTNode):
  def __init__(self, mod):
    super().__init__()
    self.mod = mod
  @property
  def module(self):
    return self.mod

class ASTComponent(ASTNode): # TODO
  @property
  def name(self): # TODO return an element of self.children

  @property
  def expressions(self): # TODO return one or more children

  def __init__(self, componentID, *args):
    self.id = componentID

    for arg in args:
      self.children.append(arg)    


class ASTInputExpr(ASTNode): # TODO
class ASTOutputExpr(ASTNode): # TODO
class ASTAssignmentExpr(ASTNode): # TODO
  @property
  def binding(self): # TODO
  @property
  def value(self): # TODO


class ASTEvalExpr(ASTNode): # TODO-check
  @property
  def op(self): # TODO
    return self.children[0]
  @property
  def args(self): # TODO
    return self.children[1:]

  def __init__(self, operator,*args):
    super().__init__()
    self.children.append(operator)

    for arg in args:
      self.children.append(arg)





# These are already complete.
class ASTID(ASTNode):
  def __init__(self, name, typedecl=None):
    super().__init__()
    self.name = name
    self.type = typedecl

class ASTLiteral(ASTNode):
  def __init__(self, value):
    super().__init__()
    self.value = value
    self.type = 'Scalar'