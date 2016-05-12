from tsdb import PersistentDB
from tsdb import DBRow
import timeseries as ts
import time

identity = lambda x: x

schema = {
  'pk': {'convert': identity, 'index': None, 'default': -1},  # Will be indexed anyways
  'ts': {'convert': identity, 'index': None, 'default': None},
  'order': {'convert': int, 'index': 1, 'default': 0},
  'blarg': {'convert': int, 'index': 1, 'default': 0},
  'useless': {'convert': identity, 'index': None, 'default': 0},
  'mean': {'convert': float, 'index': 1, 'default': 0},
  'std': {'convert': float, 'index': 1, 'default': 0},
  'vp': {'convert': bool, 'index': 1, 'default': False}
}

NUMVPS = 5

# we augment the schema by adding columns for 5 vantage points
for i in range(NUMVPS):
    schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1, 'default': 0}

# Define Time Series
t1 = [0,1,2,3,4]
v1 = [1.0,2.0,3.0,2.0,1.0]
ats1 = ts.TimeSeries(t1, v1)
    
t2 = [10,11,12,13,14]
v2 = [-1.0,-2.0,-3.0,-2.0,-1.0]
ats2 = ts.TimeSeries(t2, v2)    

t3 = [10,11,12,13,14]
v3 = [-1.0,-2.0,-3.0,-2.0,-1.0]
ats3 = ts.TimeSeries(t3, v3)    

t4 = [10,11,12,13,14]
v4 = [-2.0,-2.0,-2.0,-2.0,-2.0]
ats4 = ts.TimeSeries(t4, v4) 

db = PersistentDB(schema, 'pk', overwrite=True)
first_tid = db.begin_transaction()
assert(first_tid == 1)

# Test that modifying this tid doesn't modify sequence
first_tid += 1
assert(first_tid == 2)

second_tid = db.begin_transaction()
assert(second_tid == 2)

# db = PersistentDB(schema, 'pk', overwrite=True)
# tid = db.begin_transaction()

# db.insert_ts(tid, 1, ats1)
# db.insert_ts(tid, 2, ats2)
# db.insert_ts(tid, 3, ats3)

# db.upsert_meta(tid, 1, {'ts': ats1, 'blarg': 3, 'order': 1})
# # One result
# ids1, fields1 = db.select(tid, {'pk': {'==': 1}},['ts'],None)
# print (ids1)
# print (fields1)
# #assert(ids1 == [1])
# #assert(fields1[0]['ts'] == ats1)