from pype import lexer
from pype.lexer import tokens
import ply

# Test the pype lexer

def test_tokens():
    lexer.input('(){}')
    output = list(lexer)
    assert(output[0].type == 'LPAREN')
    assert(output[1].type == 'RPAREN')
    assert(output[2].type == 'LBRACE')
    assert(output[3].type == 'RBRACE')
    
def test_number():
    lexer.input('394')
    output = list(lexer)
    assert(output[0].type == 'NUMBER')
    assert(output[0].value == 394)
    
def test_id():
    lexer.input('anid')
    output = list(lexer)
    assert(output[0].type == 'ID')
    assert(output[0].value == 'anid')
    
def test_assign():
    lexer.input(':=')
    output = list(lexer)
    assert(output[0].type == 'ASSIGN')


