class TimeSeries:

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if len(index) != len(value):
            return 'Error'
        self.data[index] = value
	
    def __repr__(self):
        class_name = type(self).__name__
        return "%s(length=%r, first=%r, last=%r)" % (class_name, len(self.data), self.data[0], self.data[-1])
    
    def __str__(self):
        return "TimeSeries: Length - %r, First - %r, Last - %r" % (len(self.data), self.data[0], self.data[-1])

