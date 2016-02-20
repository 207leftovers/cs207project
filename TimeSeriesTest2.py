#Test from Lab 10
import numpy as np
from TimeSeries import TimeSeries
import matplotlib.pyplot as plt

# Create a non-uniform TimeSeries instance:
a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])


#These should give assertion errors
#b = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5])
#c = TimeSeries([1, 0.9, 2, 2.5, 10], [0, 2, -1, 0.5, 0])
#d = TimeSeries([1, 1, 2, 2.5, 10], [0, 2, -1, 0.5, 0])

print (a[1.5])

# Set the value at time 2.5
a[2.5] == 0.5
# Set the value at time 1.5
a[1.5] = 2.5

print (a[1.5])

# This should return an error, because there is no time point at t=0
print (a[-1])

print (a[2.3])

print (a[11])

print (-1 in a)

print (10 in a)

print (TimeSeries(range(0,10000), range(0,10000)))

x = a.times()
print (x)

y = a.values()
print (y)

z = a.items()
print (z)

print ([v for v in TimeSeries([0,1,2],[1,3,5])])

a = TimeSeries([0,5,10], [1,2,3])
b = TimeSeries([2.5,7.5], [100, -100])


#Testing Interpolations
print (a.interpolate([1]) == TimeSeries([1],[1.2]))
print (a.interpolate(b.times()) == TimeSeries([2.5,7.5], [1.5, 2.5]))
print (a.interpolate([-100,100]) == TimeSeries([-100,100], [1,3]))

smoketest = TimeSeries([0.2,0.5, 0.7, 0.9], [1,-3, 6, -4])
randompoints = np.random.random(100)
smoketest2 = smoketest.interpolate(np.sort(randompoints))
plt.plot(smoketest2.times(), smoketest2.values(), 'o')
plt.show()