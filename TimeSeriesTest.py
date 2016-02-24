from TimeSeries import TimeSeries

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

# Run the tests
test_mean()
test_median()