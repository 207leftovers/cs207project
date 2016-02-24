import numpy as np
from bisect import bisect_left
from lazy import LazyOperation

class TimeSeries:
    """
    A class to store a single, ordered set of TimeSeries data

    Parameters
    ----------
    _times
        contain the timestamps of the data
    _values
        contains the values of the data that correspond to each timestamp


    Functions
    ----------
    __init__
        Takes in user-input data and save it in the class
        Data is in the form of 2 list of equal length, containing the timestamps and the corresponding values
        Timestamp has to be monotonically increasing

        Assertion Error will be raised when
            1. the length of the two lists are different
            2. Timestamp is not monotonically increasing

    __len__
        asserts that _values and _times are of the same length
    	Returns the length of the series

    __getpos
        search for the timestamp in self._times using binary search (via bisect_left)
        throw exception errors when the timestamp is out of range or not found within the array

   	__getitem__
   		Given a time, returns the corresponding value of the series

   	__setitem__
   		Given a time, update the value corresponding the time with the input value

    __str__
        Prints the length, first element and last element of the series if the length is greater than five

    __eq__
        for two timeseries, check that all values and timestamps are equal

    __contains__
        check if a timestamp exist in the data

    __iter__
        return an instance of TimeSeriesIterator that can iterate through the values of the time series
        
    itertimes
        return an instance of TimeSeriesIterator that can iterate through the times of the time series
        
    itervalues
        see __iter__ above
       
    iteritems
        return an instance of TimeSeriesIterator that iterates over the time value pairs

    items
        return the list of (timestamp, value) tuples

    times
        return the list of timestamps

    values
        return the list of values
        
    mean
        return the mean of the values
    
    medians 
        return the median of the values


    interpolate
        Given a list of timestamps, find the interpolation value of those timestamps
        For t in list, cases considered:
            1. if t <= smallest timestamp in self, interpolation value = value of smallest timestamp
            2. if t >= largest timestamp in self, interpolation value = value of largest timestamp
            3. if t == some timestamp in self, interpolation value = value of that timestamp
            4. if t is between a pair of timestamps, value is the interpolated values between the two nearest timestamps
    """
    def __init__(self, times, values):

        #times and values are 2 arrays that match to each other. Check that they have the same length
        assert len(times) == len(values)

        #Check that the list of time is monotonically increasing
        assert all(times[i] < times[i+1] for i in range(len(times)-1))

        self._times = np.array(times)
        self._values = np.array(values)


    def __len__(self):

        #_times and _values are 2 arrays that match to each other. Check that they have the same length
        assert len(self._times) == len(self._values)
        return len(self._values)


    def __getpos(self, time):
        if time > self._times[-1] or time < self._times[0]:
            raise IndexError("IndexError: Timestamp out of range of data: "+ str(time))

        #Do a binary search to find the position to the left of the time
        pos = bisect_left(self._times,time)

        #Check that the position correspond to the actual value. otherwise throw an error
        if self._times[pos] != time:
            raise ValueError("ValueError: Value not found in timestamps: " + str(time))
        return pos

    def __getitem__(self, time):

        try:
            pos = self.__getpos(time)
            return self._values[pos]
        except Exception as exc:
            print (exc)


    def __setitem__(self, time, value):

        try:
            pos = self.__getpos(time)
            self._values[pos] = value
        except Exception as exc:
            print (exc)

    def __contains__(self, time):

        try:
            pos = self.__getpos(time)
            return True
        except Exception as exc:
            return False

    def __repr__(self):
        return "%r" %(self._values)

    def __str__(self):
    	if len(self._values) > 5:
    		return "TimeSeries: Length - %r, First - %r, Last - %r" % (len(self._values), self._values[0], self._values[-1])
    	else:
    		return "TimeSeries: (%r, %r)" %(list(self._times), list(self._values))

    def __iter__(self):
        return TimeSeriesIterator(self._values)
    
    def itertimes(self):
        return TimeSeriesIterator(self._times)
    
    def itervalues(self):
        return TimeSeriesIterator(self._values)
    
    def iteritems(self):
        combined = []
        for i in range(len(self._times)):
            combined.append((self._times[i], self._values[i]))
        return TimeSeriesIterator(combined)

    #check for equality, elementwise for both _times and _values
    def __eq__(self, other):
        return (self._values==other._values).all() and (self._times==other._times).all()

    def values(self):
        return list(self._values)

    def times(self):
        return list(self._times)

    def items(self):
        return list(zip(self._times, self._values))
    
    def mean(self):
        return np.mean(self._values)
    
    def median(self):
        return np.median(self._values)

    def interpolate(self, time_points):

        value_points = np.zeros(len(time_points))
        val_index = 0

        for time in time_points:

            #Check right boundary
            if time >= self._times[-1]:
                value_points[val_index] = self._values[-1]

            #Check Left boundary
            elif time <= self._times[0]:
                value_points[val_index] = self._values[0]
            else:
                pos = bisect_left(self._times,time)

                #check if the timestamp exist in _time array
                if self._times[pos] == time:
                    value_points[val_index] = self._values[pos]

                #if it does not exist, do interpolation
                else:
                    right = self._times[pos]
                    left = self._times[pos-1]
                    right_val = self._values[pos]
                    left_val = self._values[pos-1]
                    gradient = (right_val-left_val)/(right - left)
                    value_points[val_index] = (time - left) * gradient + left_val

            val_index += 1

        #Create a new instance of TimeSeries with the interpolated values
        return TimeSeries(time_points,value_points)

    @property
    def lazy(self):
        return LazyOperation(self)

    def __call__(self):
        return self

class TimeSeriesIterator:
    '''
    This is an iterator for the TimeSeries class to iterate through the values of the time series
    '''
    def __init__(self, values):
        self._values = values
        self.index = 0

    def __next__ (self):
        try:
            val = self._values[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return val

    def __iter__(self):
        return self
