from tsdb import DictDB
import timeseries as ts

identity = lambda x: x

schema = {
  'pk': {'convert': identity, 'index': None},  #will be indexed anyways
  'ts': {'convert': identity, 'index': None},
  'order': {'convert': int, 'index': 1},
  'blarg': {'convert': int, 'index': 1},
  'useless': {'convert': identity, 'index': None},
  'mean': {'convert': float, 'index': 1},
  'std': {'convert': float, 'index': 1},
  'vp': {'convert': bool, 'index': 1}
}

NUMVPS = 5

# we augment the schema by adding columns for 5 vantage points
for i in range(NUMVPS):
    schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}

def test_insert():
    db = DictDB(schema, 'pk')
    
    t = [0,1,2,3,4]
    v = [1.0,2.0,3.0,2.0,1.0]
    ats = ts.TimeSeries(t, v)
    
    db.insert_ts(1, ats)
    
    rows = db.rows
    assert(rows[1] is not None)
    assert(rows[1]['pk'] == 1)
    assert(rows[1]['ts'] == ats)
    
    try:
        db.insert_ts(1, ats)
    except Exception as e: 
        e1 = e
    assert str(e1) == 'Duplicate primary key found during insert'
    assert type(e1).__name__ == 'ValueError'  
    
def test_upsert():
    db = DictDB(schema, 'pk')
    
    t1 = [0,1,2,3,4]
    v1 = [1.0,2.0,3.0,2.0,1.0]
    ats1 = ts.TimeSeries(t1, v1)
    
    t2 = [10,11,12,13,14]
    v2 = [-1.0,-2.0,-3.0,-2.0,-1.0]
    ats2 = ts.TimeSeries(t2, v2)
    
    db.insert_ts(1, ats1)
    db.insert_ts(2, ats1)
    
    db.upsert_meta(2, {'ts': ats2})
    db.upsert_meta(3, {'ts': ats2, 'not_there': 3, 'order': 1})
    
    rows = db.rows
    
    assert(rows[1]['ts'] == ats1)
    assert(rows[2]['ts'] == ats2)
    assert(rows[3]['ts'] == ats2)
    assert(rows[3]['order'] == 1)