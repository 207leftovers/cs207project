class ASTVisitor():
  def visit(self, astnode):
    'A read-only function which looks at a single AST node.'
    pass
  def return_value(self):
    return None


class ASTModVisitor(ASTVisitor):
  '''A visitor class that can also construct a new, modified AST.
  Two methods are offered: the normal visit() method, which focuses on analyzing
  and/or modifying a single node; and the post_visit() method, which allows you
  to modify the child list of a node.
  The default implementation does nothing; it simply builds up itself, unmodified.'''
  def visit(self, astnode):
    # Note that this overrides the super's implementation, because we need a
    # non-None return value.
    return astnode
  def post_visit(self, visit_value, child_values):
    '''A function which constructs a return value out of its children.
    This can be used to modify an AST by returning a different or modified
    ASTNode than the original. The top-level return value will then be the
    new AST.'''
    return visit_value




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
    print(indent + self.__class__.__name__)
    indent = indent + '   '
    for child in self._children:
      child.pprint(indent)


  def walk(self, visitor):
    '''Traverses an AST, calling visitor.visit() on every node.

    This is a depth-first, pre-order traversal. Parents will be visited before
    any children, children will be visited in order, and (by extension) a node's
    children will all be visited before its siblings.
    The visitor may modify attributes, but may not add or delete nodes.'''
    visitor.visit(self)
    for child in self.children:
      child.walk(visitor)

    return visitor.return_value()


  def mod_walk(self, mod_visitor):
    '''Traverses an AST, building up a return value from visitor methods.
    Similar to walk(), but constructs a return value from the result of
    postvisit() calls. This can be used to modify an AST by building up the
    desired new AST with return values.'''

    selfval = mod_visitor.visit(self)
    child_values = [child.mod_walk(mod_visitor) for child in self.children]
    retval = mod_visitor.post_visit(self, selfval, child_values)
    return retval



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

class ASTComponent(ASTNode):
  def __init__(self, component_id, expression_list=[]):
    super().__init__()
    self.children.append(component_id)
    for expression in expression_list:
      self.children.append(expression)

  @property
  def name(self): # return an element of self.children
    return self.children[0]

  @property
  def expressions(self): # return one or more children
    return self.children[1:]

class ASTInputExpr(ASTNode):
  def __init__(self, input_list):
    super().__init__()
    for input_i in input_list:
      self.children.append(input_i)
    
class ASTOutputExpr(ASTNode):
  def __init__(self, output_list):
    super().__init__()
    for output_i in output_list:
      self.children.append(output_i)
    
class ASTAssignmentExpr(ASTNode): 
  def __init__(self, expression_id, expression):
    super().__init__()
    self.children.append(expression_id)
    self.children.append(expression)

  @property
  def binding(self):
    return self.children[0]
  @property
  def value(self):
    return self.children[1]

class ASTEvalExpr(ASTNode):
  def __init__(self, operator, parameter_list=[]):
    super().__init__()
    self.children.append(operator)
    for parameter in parameter_list:
        self.children.append(parameter)
    
  @property
  def op(self):
    return self.children[0]
  @property
  def args(self):
    return self.children[1:]

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
