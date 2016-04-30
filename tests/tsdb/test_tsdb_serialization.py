from tsdb import *
import json
import timeseries as ts
from tsdb import TSDBOp

def test_serialize():
    
    t = [0,1,2,3,4]
    v = [1.0,2.0,3.0,2.0,1.0]
    ats = ts.TimeSeries(t, v)
    
    data_dict = {}
    data_dict['pk'] = 1
    data_dict['ts'] = ats
    
    obj = TSDBOp.to_json(data_dict)
    
    # Serialize
    s = serialize(obj)
    s_half = len(s)//2
    
    first_half = s[:s_half]
    second_half = s[s_half:]
    
    # Deserialize
    # Break with only first half
    d = Deserializer()
    d.append(first_half)
    first_ready = d.ready()
    assert(first_ready == False)
    r = d.deserialize()
    assert(r == None)
    
    # Now re-try with both halves
    d.append(first_half)
    d.append(second_half)
    second_ready = d.ready()
    assert(second_ready == True)
    r = d.deserialize()
    assert(obj == r)