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

# Test that unnecessary assignment nodes are being removed
def test_assignment_ellision():
    ir.flowgraph_pass( AssignmentEllision() )
    standardize_graph = ir.graphs['standardize']
    nodes_to_have = ['@N0', '@N1', '@N3', '@N5', '@N6', '@N8']
    
    assert(len(standardize_graph.nodes) == len(nodes_to_have))
    
    for node in nodes_to_have:
        assert(node in standardize_graph.nodes)
    
    for a_var in standardize_graph.variables.keys():
        assert(standardize_graph.variables[a_var] in nodes_to_have)

# Test that code that doesn't contribute to outputs is removed
def test_dead_code_elimination1():
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
        
# Test that code that doesn't contribute to outputs is removed
def test_dead_code_elimination2():
    deadcodeinput = """(import timeseries)
    { mul (input x y) (:= z (* x y)) (output z) }
    { dist (input a b) (:= c (mul (mul a b) (mul b a))) (output c) }"""

    ast2 = parser.parse(deadcodeinput, lexer=lexer)
    syms2 = ast2.walk( SymbolTableVisitor() )
    ir2 = ast2.mod_walk( LoweringVisitor(syms2) )    
    ir2.flowgraph_pass( DeadCodeElimination() )

    # Check the 'mul' graph
    component_graph1 = ir2.graphs['mul']
    nodes_to_have1 = ['@N0', '@N1', '@N2', '@N3', '@N4']
    assert(len(component_graph1.nodes) == len(nodes_to_have1))
    for node in nodes_to_have1:
        assert(node in component_graph1.nodes)
    for a_var in component_graph1.variables.keys():
        assert(component_graph1.variables[a_var] in nodes_to_have1)
    assert(len(component_graph1.outputs) == 1)
        
    # Check the 'dist' graph
    component_graph2 = ir2.graphs['dist']
    nodes_to_have2 = ['@N0', '@N1', '@N2', '@N3', '@N4', '@N5', '@N6']
    assert(len(component_graph2.nodes) == len(nodes_to_have2))
    for node in nodes_to_have2:
        assert(node in component_graph2.nodes)
    for a_var in component_graph2.variables.keys():
        assert(component_graph2.variables[a_var] in nodes_to_have2)
    assert(len(component_graph2.outputs) == 1)

# Test that the provided inlining code is functioning appropriately
def test_inline():
    with open ('tests/pype/test_cases/example_opt.ppl') as f:
        opt_ppl = f.read()
    program_input ='''
    (import timeseries)
    { mul (input x y) (:= z (* x y)) (output z) }
    { dist (input a b) (:= c (mul (mul a b) (mul b a))) (output c) }
    '''
    ast3 = parser.parse(program_input, lexer=lexer)
    ast3.walk(CheckSingleAssignment())
    ast3.walk(CheckSingleIOExpression())
    syms3 = ast3.walk( SymbolTableVisitor() )
    ast3.walk(CheckUndefinedVariables(syms3))
    ir3 = ast3.mod_walk( LoweringVisitor(syms3) )
    ir3.flowgraph_pass( AssignmentEllision() )
    ir3.flowgraph_pass( DeadCodeElimination() )
    ir3.topological_flowgraph_pass(InlineComponents())
