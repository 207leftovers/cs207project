class TimeSeries:
    """
    A class to store a single, ordered set of numerical data

    Parameters
    ----------
    data: list
        A list of single, ordered numerical data

    Functions
    ----------
    __init__
        Takes in user-input data and save it in the class

    __str__
        return the length, first element and last element of the data


    """
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if index > len(self.data):
            return 'Error'
        self.data[index] = value
	
    def __repr__(self):
        return "TimeSeries(length=%r, first=%r, last=%r)" % (len(self.data), self.data[0], self.data[-1])
    
    def __str__(self):
        return "TimeSeries: Length - %r, First - %r, Last - %r" % (len(self.data), self.data[0], self.data[-1])

