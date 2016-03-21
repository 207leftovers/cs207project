class ArrayTimeSeries(TimeSeries):
    
    def __init__(self, data):
        self._data = np.array(data)