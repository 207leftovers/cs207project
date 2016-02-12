class TimeSeries:
    """
    A class to store a single, ordered set of numerical data

    Parameters
    ----------
    data: 
        Any object that can be treated like a sequence

    Functions
    ----------
    __init__
        Takes in user-input data and save it in the class

    __len__
    	Returns the length of the series

   	__getitem__
   		Given an index, returns the corresponding value of the series

   	__setitem__
   		Given an index, update the value corresponding the index with the input value

    __str__
        return the length, first element and last element of the series


    """
    def __init__(self, data):
        self._data = list(data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        if index >= len(self._data):
            return 'Error'
        self._data[index] = value
	
    def __repr__(self):
        return "TimeSeries(length=%r, first=%r, last=%r)" % (len(self.data), self.data[0], self.data[-1])
    
    def __str__(self):
        return "TimeSeries: Length - %r, First - %r, Last - %r" % (len(self.data), self.data[0], self.data[-1])

