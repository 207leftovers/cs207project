import pype
import sys

filename1 = 'test_cases/example1.ppl'
outputfile1 = 'test_cases/example1.ast'
def test_example1(filename1, outputfile1):
  testAST = pype.TestPipeline(source=filename1)
  ASTList = testAST.return_out()

  refList = []
  with open(outputfile1) as f:
    lines = f.readlines()
    for line in lines:
        refList.append(line.strip())

  assert(refList == ASTList)


filename2 = 'test_cases/example0.ppl'
outputfile2 = 'test_cases/example0.ast'
def test_example2(filename2, outputfile2):
  testAST = pype.TestPipeline(source=filename2)
  ASTList = testAST.return_out()

  refList = []
  with open(outputfile2) as f:
    lines = f.readlines()
    for line in lines:
        refList.append(line.strip())

  assert(refList == ASTList)

