from tsdb import PersistentDB
from tsdb import DBRow
import timeseries as ts
import time
import unittest

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

# Define Time Series
t1 = [0,1,2,3,4]
v1 = [1.0,2.0,3.0,2.0,1.0]
ats1 = ts.TimeSeries(t1, v1)
    


db = PersistentDB(schema, 'pk', overwrite=True)
first_tid = db.begin_transaction()
db.insert_ts(first_tid, 1, ats1)
row1 = DBRow.row_from_string(db._trees['pk'].get(1))
assert(row1.pk == 1)
assert(db._trees['pk'].has_key(1) == True)

#COMMIT 
db.commit(first_tid)

# ROLLBACK
try:
	db.rollback(first_tid)
except Exception as e: 
    e1 = e
assert type(e1).__name__ == 'ValueError'  

#Add Meta Data
second_tid = db.begin_transaction()

db.upsert_meta(second_tid, 1, { 'order': 1})

ids1, fields1 = db.select(second_tid, {'pk': {'==': 1}}, ['ts', 'order'], None)
assert(ids1 == [1])
assert(fields1[0]['ts'] == ats1)
assert(fields1[0]['order'] == 1)
print (fields1)
db.rollback(second_tid)

third_tid = db.begin_transaction()
ids1, fields1 = db.select(third_tid, {'pk': {'==': 1}}, ['ts', 'order'], None)
print (fields1)
assert(ids1 == [1])
assert(fields1[0]['ts'] == ats1)
assert(fields1[0]['order'] == 0.0)
