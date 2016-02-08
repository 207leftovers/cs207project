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


