from .lexer import lexer
from .parser import parser
from .ast import *
#from .semantic_analysis import CheckSingleAssignment
#from .translate import SymbolTableVisitor

from io import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


class TestPipeline(object):
  def __init__(self, source):
    with open(source) as f:
      self.compile(f)

  def compile(self, file):
    input = file.read()
    ast = parser.parse(input, lexer=lexer)
    with Capturing() as output:
      ast.pprint()
    out = [k.strip() for k in output]
    self.out = out

  def return_out(self):
      return self.out
