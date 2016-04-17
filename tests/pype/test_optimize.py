from pype import fgir
from pype.translate import SymbolTableVisitor, LoweringVisitor
from pype import lexer
from pype import parser
from pype import ast
from pype.semantic_analysis import CheckSingleAssignment, CheckSingleIOExpression, PrettyPrint, CheckUndefinedVariables
from pype.optimize import *

input1 = """(import timeseries)
{ standardize
  (input (TimeSeries t))
  (:= mu (mean t))
  (:= sig (std t))
  (:= new_t (/ (- t mu) sig))
  (output new_t)
}"""
    
ast = parser.parse(input1, lexer=lexer)
syms = ast.walk( SymbolTableVisitor() )
ir = ast.mod_walk( LoweringVisitor(syms) )    

def test_assignment_ellision():
    ir.flowgraph_pass( AssignmentEllision() )
    standardize_graph = ir.graphs['standardize']
    nodes_to_have = ['@N0', '@N1', '@N3', '@N5', '@N6', '@N8']
    
    assert(len(standardize_graph.nodes) == len(nodes_to_have))
    
    for node in nodes_to_have:
        assert(node in standardize_graph.nodes)
    
    for a_var in standardize_graph.variables.keys():
        assert(standardize_graph.variables[a_var] in nodes_to_have)

def test_dead_code_elimination():
    deadcodeinput = """{ component
      (input x)
      (:= useless 1)
      (output x)
    }"""

    ast2 = parser.parse(deadcodeinput, lexer=lexer)
    syms2 = ast2.walk( SymbolTableVisitor() )
    ir2 = ast2.mod_walk( LoweringVisitor(syms2) )    
    
    ir2.flowgraph_pass( DeadCodeElimination() )
    component_graph = ir2.graphs['component']
    nodes_to_have = ['@N0', '@N3']

    assert(len(component_graph.nodes) == len(nodes_to_have))
    
    for node in nodes_to_have:
        assert(node in component_graph.nodes)

    for a_var in component_graph.variables.keys():
        assert(component_graph.variables[a_var] in nodes_to_have)