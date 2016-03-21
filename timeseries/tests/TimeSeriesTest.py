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
    
    
# Test Operators
def test_add():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    b = TimeSeries([1, 1.5, 2, 2.5, 10], [1, 2, 3, 4, 5])
    c = TimeSeries([1, 1.5, 2, 3, 10], [1, 2, 3, 4, 5])
    d = TimeSeries([1, 1.5, 2, 10], [1, 2, 3, 5])
    assert a+b == TimeSeries([1, 1.5, 2, 2.5, 10], [1, 4, 2, 4.5, 5])
    assert a+3 == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [3.0, 5.0, 2.0, 3.5, 3.0])
    assert 3+a == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [3.0, 5.0, 2.0, 3.5, 3.0])
    
    # Test that the timepoints are the same
    e1 = ''
    try:
        a + c
    except Exception as e: 
        e1 = e
    assert str(e1) == 'TimeSeries: ([1.0, 1.5, 2.0, 2.5, 10.0], [0.0, 2.0, -1.0, 0.5, 0.0]) and TimeSeries: ([1.0, 1.5, 2.0, 3.0, 10.0], [1, 2, 3, 4, 5]) must have the same time points'
    assert type(e1).__name__ == 'ValueError'
    
    # Test that they have the same number of timepoints
    e2 = ''
    try:
        a + d
    except Exception as e: 
        e2 = e
    assert str(e2) == 'TimeSeries: ([1.0, 1.5, 2.0, 2.5, 10.0], [0.0, 2.0, -1.0, 0.5, 0.0]) and TimeSeries: ([1.0, 1.5, 2.0, 10.0], [1, 2, 3, 5]) must have the same time points' 
    assert type(e2).__name__ == 'ValueError'
    
    # Test that they have time series
    e3 = ''
    try:
        a + [0, 1, 2, 3, 4]
    except Exception as e: 
        e3 = e
    print(type(e3))
    #assert type(e3).__name__ == 'AttributeError'
    #assert str(e3) == "'list' object has no attribute '_values'" 
        
def test_sub():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    b = TimeSeries([1, 1.5, 2, 2.5, 10], [1, 2, 3, 4, 5])
    assert a-b == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [-1.0, 0.0, -4.0, -3.5, -5.0])
    assert 3-a == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [3.0, 1.0, 4.0, 2.5, 3.0])
    assert a-3 == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [-3.0, -1.0, -4.0, -2.5, -3.0])
    
def test_mul():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    b = TimeSeries([1, 1.5, 2, 2.5, 10], [1, 2, 3, 4, 5])
    assert a*b == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [0.0, 4.0, -3.0, 2.0, 0.0])
    assert 3*a == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [0.0, 6.0, -3.0, 1.5, 0.0])
    assert a*3 == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [0.0, 6.0, -3.0, 1.5, 0.0])
    
def test_unary():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    assert abs(a) == 2.29128784747792
    assert bool(a) == True
    assert -a == TimeSeries([1.0, 1.5, 2.0, 2.5, 10.0], [-0.0, -2.0, 1.0, -0.5, -0.0])
    assert +a == TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    
# Run the tests
print("Running mean and median tests")
test_mean()
test_median()

print("Running iteration tests")
test_iter()
test_itertimes()
test_itervalues()
test_iteritems()

print("Running operations")
test_add()
test_sub()
test_mul()
test_unary()
