import numpy as np
from TimeSeries import TimeSeries
import matplotlib.pyplot as plt

# Create a non-uniform TimeSeries instance:
a = TimeSeries([1, 1.5, 2, 2.5, 10], [0, 2, -1, 0.5, 0])

b = TimeSeries([1, 1.5, 2, 2.5, 10], [1, 2, 3, 4, 5])

c = TimeSeries([1, 1.5, 2, 3, 10], [1, 2, 3, 4, 5])

d = TimeSeries([1, 1.5, 2, 10], [1, 2, 3, 5])

print (a+b)

try:
	print (a+c)
except Exception as e:
	print (type(e),e)

try:
	print (a+d)
except Exception as e:
	print (type(e),e)

print (a+3)

print (3+a)

print (abs(a))

print (bool(a))

print (-a)

print (+a)

print (a-3)

print (3-a)

print (a-b)

print (a*3)

print (3*a)

print (a*b)