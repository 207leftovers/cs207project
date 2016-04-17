from pype import fgir
from pype.translate import SymbolTableVisitor, LoweringVisitor

from pype.optimize import *

from pype import lexer
from pype import parser
from pype import ast
from pype.semantic_analysis import CheckSingleAssignment, CheckSingleIOExpression, PrettyPrint, CheckUndefinedVariables
from timeseries import TimeSeries

input = """(import timeseries)

{ standardize
  (input (TimeSeries t))
  (:= mu (mean t))
  (:= sig (std t))
  (:= new_t (/ (- t mu) sig))
  (output new_t)
}"""
    
ast = parser.parse(input, lexer=lexer)
syms = ast.walk( SymbolTableVisitor() )
ir = ast.mod_walk( LoweringVisitor(syms) )    
standardize_graph = ir.graphs['standardize']
    
def test_nodes():
    assert(standardize_graph.nodes['@N0'].nodeid == '@N0')
    assert(standardize_graph.nodes['@N0'].inputs == [])
    assert(standardize_graph.nodes['@N0'].ref == None)
    assert(standardize_graph.nodes['@N0'].__repr__() == '<FGNodeType.input @N0<= : None>')
    
    assert(standardize_graph.nodes['@N1'].nodeid == '@N1')
    assert(standardize_graph.nodes['@N1'].inputs == ['@N0'])
    assert(standardize_graph.nodes['@N1'].ref == TimeSeries.mean)
    
    assert(standardize_graph.nodes['@N2'].nodeid == '@N2')
    assert(standardize_graph.nodes['@N2'].inputs == ['@N1'])
    assert(standardize_graph.nodes['@N2'].ref == None)
    
    assert(standardize_graph.nodes['@N3'].nodeid == '@N3')
    assert(standardize_graph.nodes['@N3'].inputs == ['@N0'])
    assert(standardize_graph.nodes['@N3'].ref == TimeSeries.std)
    
    assert(standardize_graph.nodes['@N4'].nodeid == '@N4')
    assert(standardize_graph.nodes['@N4'].inputs == ['@N3'])
    assert(standardize_graph.nodes['@N4'].ref == None)
    
    assert(standardize_graph.nodes['@N5'].nodeid == '@N5')
    assert(standardize_graph.nodes['@N5'].inputs == ['@N0', '@N2'])
    assert(standardize_graph.nodes['@N5'].ref == TimeSeries.__sub__)
    
def test_topological_sort():
    dotfile = standardize_graph.dotfile()
    sorted_nodes = standardize_graph.topological_sort()
    
    # Ensure that the dotfile print out hasn't been affected by topological sort
    assert(dotfile == standardize_graph.dotfile())
    
    # Check input is first
    assert(sorted_nodes[0] == '@N0')
    
    # Check output is last
    assert(sorted_nodes[-1] == '@N8')
    
    # Check some orderings
    assert(sorted_nodes.index('@N5') > sorted_nodes.index('@N0'))
    assert(sorted_nodes.index('@N5') > sorted_nodes.index('@N2'))
    assert(sorted_nodes.index('@N4') > sorted_nodes.index('@N3'))
    assert(sorted_nodes.index('@N2') > sorted_nodes.index('@N1'))
    assert(sorted_nodes.index('@N1') > sorted_nodes.index('@N0'))
