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
        return "%s(length=%r)" % (class_name, self.__len__)
    
    def __str__(self):
	l = __len__
        return "TimeSeries: Length - " + l + ", First - " + self.data[0] + ", Last - " + self.data[l - 1]

