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
    print()
    ir.flowgraph_pass( AssignmentEllision() )
    standardize_graph = ir.graphs['standardize']
    nodes_to_have = ['@N0', '@N1', '@N3', '@N5', '@N6', '@N8']
    for key in ir.graphs.keys():
        print("Graph for: ", key)
        print(ir.graphs[key].dotfile())
    assert(len(standardize_graph.nodes) == len(nodes_to_have))
    print(standardize_graph.nodes)
    for node in nodes_to_have:
        assert(node in standardize_graph.nodes)
        

def test_dead_code_elimination():
    ir.flowgraph_pass( DeadCodeElimination() )
    standardize_graph = ir.graphs['standardize']
    

