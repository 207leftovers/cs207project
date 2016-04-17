from pype import lexer
from pype import parser
from pype import ast
from pype import semantic_analysis
from pype.translate import SymbolTableVisitor

def test_single_component_assignment():
    input = """{ comp1 (input) (output) (:= a 1) }
{ comp1 (input) (output) (:= a 2) }"""
    
    ast = parser.parse(input, lexer=lexer)
    
    # Catch the double component assigment
    try:
        ast.walk( semantic_analysis.CheckSingleAssignment() )
    except Exception as e: 
        e1 = e
    assert str(e1) == 'Component name: comp1 has already been taken'
    assert type(e1).__name__ == 'PypeSyntaxError'
    
def test_single_node_assignment():
    input="""(import timeseries)

    { standardize
      (input (TimeSeries t))
      (:= mu (mean t))
      (:= t (std t))
      (:= new_t (/ (- t mu) sig))
      (output new_t)
    }"""
    
    ast = parser.parse(input, lexer=lexer)
    
    # Catch the double node assigment
    try:
        ast.walk( semantic_analysis.CheckSingleAssignment() )
    except Exception as e: 
        e1 = e
    assert str(e1) == 'Node name: t has already been taken'
    assert type(e1).__name__ == 'PypeSyntaxError'  
    
def test_single_node_input_assignment():
    input="""(import timeseries)

    { standardize
      (input (TimeSeries t1))
      (input (TimeSeries t1))
      (output)
    }"""
    
    ast = parser.parse(input, lexer=lexer)
    
    # Catch the double input assigment
    try:
        ast.walk( semantic_analysis.CheckSingleAssignment() )
    except Exception as e: 
        e1 = e
    assert str(e1) == 'Node name: t1 has already been taken'
    assert type(e1).__name__ == 'PypeSyntaxError'  
    
def test_multiple_inputs():
    input="""(import timeseries)

    { standardize
      (input (TimeSeries t1))
      (input (TimeSeries t2))
      (output)
    }"""
    
    ast = parser.parse(input, lexer=lexer)
    
    # Catch multiple inputs
    try:
        ast.walk( semantic_analysis.CheckSingleIOExpression() )
    except Exception as e: 
        e1 = e
    assert str(e1) == 'Component standardize has multiple input expressions'
    assert type(e1).__name__ == 'PypeSyntaxError'  
    
def test_multiple_outputs():
    input="""(import timeseries)

    { standardize
      (input (TimeSeries t1))
      (output t1)
      (output t1)
    }"""
    
    ast = parser.parse(input, lexer=lexer)
    
    # Catch multiple outputs
    try:
        ast.walk( semantic_analysis.CheckSingleIOExpression() )
    except Exception as e: 
        e1 = e
    assert str(e1) == 'Component standardize has multiple output expressions'
    assert type(e1).__name__ == 'PypeSyntaxError'

def test_check_undefined_vars():
    input="""(import timeseries)

    { standardize
      (input)
      (:= t (std1 t))
      (output)
    }"""
    
    ast = parser.parse(input, lexer=lexer)

    # Catch the undefined var
    try:
        syms = ast.walk( SymbolTableVisitor() )
        print(syms)
        ast.walk( semantic_analysis.CheckUndefinedVariables(syms) )
    except Exception as e: 
        e1 = e
    print(e1)
    assert str(e1) == 'Undefined variable: std1'
    assert type(e1).__name__ == 'PypeSyntaxError'  