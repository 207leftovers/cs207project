from timeseries.TimeSeries import TimeSeries
import numpy as np

def test_initialization():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    assert isinstance(a, TimeSeries)
    assert a == TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    
def test_len():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    assert len(a) == 5

def test_getter_setter():
    a = TimeSeries([2.5],[0.5])
    assert a[2.5] == 0.5
    # better have testing setter a[3] = 1

def test_calling():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    assert a.times() == [1, 1.5, 2, 2.5, 10]
    assert a.values() == [0, 2, -1, 0.5, 0]

# Test the Mean and Median Functions
def test_mean():
    ten = TimeSeries(range(0,11), range(0,11))    
    assert ten.mean() == 5
    
def test_std():
    ten = TimeSeries([1, 2, 3, 4, 5], [600, 470, 170, 430, 300]) 
    print(ten.std())
    assert int(ten.std()) == 147
    
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
    assert type(e3).__name__ == 'AttributeError'
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

def test_interpolation():
    a = TimeSeries([0,5,10], [1,2,3])
    b = TimeSeries([2.5,7.5], [100, -100])
    assert (a.interpolate([1]) == TimeSeries([1],[1.2]))
    assert (a.interpolate(b.times()) == TimeSeries([2.5,7.5], [1.5, 2.5]))
    assert (a.interpolate([-100,100]) == TimeSeries([-100,100], [1,3]))

def test_lazy():
    x = TimeSeries([1,2,3,4],[1,4,9,16])
    assert x == x.lazy.eval()
    
def test_contains():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    assert a.__contains__(1.5) == True
    e3 = ''
    try:
        a.__contains__('monkeys')
    except Exception as e: 
        e3 = e
    assert type(e3).__name__ == 'str'
    
def test_interpolate():
    a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
    assert a.interpolate([2]) == TimeSeries([2],[-1])