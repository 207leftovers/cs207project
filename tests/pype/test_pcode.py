#!/usr/bin/env python3
#import pype
import sys
from pype.pipeline import *
from timeseries.TimeSeries import TimeSeries
from pype.pcode import PCodeGenerator
input1 = """(import timeseries)
{ standardize
  (input (TimeSeries t))
  (:= mu (mean t))
  (:= sig (std t))
  (:= new_t (/ (- t mu) sig))
  (output new_t)
}"""

def test_pype4_final():
	time = []
	values = []

	for x in range(100):
		time.append(x)
		values.append(x-50)
	a = TimeSeries(time, values)


	ast = parser.parse(input1, lexer=lexer)

    # Semantic analysis
	ast.walk( CheckSingleAssignment() )
	ast.walk( CheckSingleIOExpression() )
	syms = ast.walk( SymbolTableVisitor() )
	ast.walk( CheckUndefinedVariables(syms) )

    
    # Translation
	ir = ast.mod_walk( LoweringVisitor(syms) )
    
	ir.flowgraph_pass( AssignmentEllision() )
	ir.flowgraph_pass( DeadCodeElimination() )
	ir.topological_flowgraph_pass( InlineComponents() )
    
    # PCode Generation
	pcodegen = PCodeGenerator()
	ir.flowgraph_pass( pcodegen )
	pcodes = pcodegen.pcodes
	standardized_TS = pcodes['standardize'].run(a)

	#print("Output should be 0, 1")
	#print("Output:", standardized_TS.mean(), standardized_TS.std())
	assert(round(standardized_TS.mean(), 7) == 0)
	assert(round(standardized_TS.std()-1, 7) == 0)