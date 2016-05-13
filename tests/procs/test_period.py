import numpy as np
from procs import period
import timeseries as ts

def basic_irregular(stopTime, numPoints, numSelPoints):
    time = np.linspace(0, stopTime, numPoints)
    data = np.sin(time)
    index = np.sort(np.random.choice(range(numPoints), size=numSelPoints, replace=False))
    time_irr = time[index]
    data_irr = data[index]
    return data_irr, time_irr


def test_p():
    stopTime = 20
    numPoints = 200
    numSelPoints = 60
    t2 = [1, 2, 3, 4]
    v2 = [40, 50, 60, 70]
    row = {}
    data_irr, time_irr = basic_irregular(stopTime, numPoints, numSelPoints)
    row['ts'] = ts.TimeSeries(time_irr, data_irr)
    print(period.proc_main(1, row, (t2, v2))[0])
    assert(np.abs(period.proc_main(1, row, (t2, v2))[0] - 6.28) < 0.5)


