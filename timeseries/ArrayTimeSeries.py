from timeseries.TimeSeries import TimeSeries
import numpy as np
class ArrayTimeSeries(TimeSeries):
    
    def __init__(self, data):
        self._data = np.array(data)
