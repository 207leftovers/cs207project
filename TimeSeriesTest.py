from TimeSeries import TimeSeries
import numpy as np

# projecteuler.net/problem=1
# Note: this is decidely *not* the intended purpose of this class.

threes = TimeSeries(range(0,1000,3), range(0,1000,3))
fives = TimeSeries(range(0,1000,5), range(0,1000,5))

s = 0
for i in range(0,1000):
  if i in threes or i in fives:
    s += i

print("sum",s)

print(repr(threes))
print(threes)

print(TimeSeries(range(0,1000000), range(0,1000000)))


# Test the Mean and Median Functions
def test_mean():
    ten = TimeSeries(range(0,11), range(0,11))    
    assert ten.mean() == 5
    
def test_median():
    median = TimeSeries(range(0,3), range(0,3))    
    assert median.median() == 1

# Test the Iterator Functions
def test_iter():
    ten = TimeSeries(range(0,11), range(0,11))  
    i = ten.__iter__()
    n = next(i)
    assert n == 0
    assert n.dtype == np.int64
    
def test_itertimes():
    ten = TimeSeries(range(0,11), range(0,11))  
    i = ten.itertimes()
    n = next(i)
    assert n == 0
    assert n.dtype == np.int64
    n = next(i)
    assert n == 1
    assert n.dtype == np.int64
    
def test_itervalues():
    ten = TimeSeries(range(0,11), range(0,11))  
    i = ten.itervalues()
    n = next(i)
    assert n == 0
    assert n.dtype == np.int64
    n = next(i)
    assert n == 1
    assert n.dtype == np.int64
    
def test_iteritems():
    ten = TimeSeries(range(0,11), range(0,11))  
    i = ten.iteritems()
    n = next(i)
    assert n == (0, 0)
    assert len(n) == 2
    assert n[0] == 0
    assert n[1] == 0
    n = next(i)
    assert n == (1, 1)
    
# Run the tests
print("Running mean and median tests")
test_mean()
test_median()

print("Running iteration tests")
test_iter()
test_itertimes()
test_itervalues()
test_iteritems()
