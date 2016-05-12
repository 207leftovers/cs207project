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

schema2 = {
  'pk': {'convert': identity, 'index': None, 'default': 0},  # Will be indexed anyways
}

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
tid = db.begin_transaction()

db.insert_ts(tid, 1, ats1)
db.insert_ts(tid, 2, ats2)
db.insert_ts(tid, 0, ats4)

pk_tree = db._trees['pk']
base_node = pk_tree._follow(pk_tree._tree_ref)
right_node = pk_tree._follow(base_node.right_ref)

row1 = DBRow.row_from_string(pk_tree._follow(base_node.value_ref))
assert(row1.pk == 1)
assert(row1.ts == ats1)

row2 = DBRow.row_from_string(pk_tree._follow(right_node.value_ref))
assert(row2.pk == 2)
assert(row2.ts == ats2)

e1 = ''
try:
    db.insert_ts(tid, 1, ats1)
except Exception as e: 
    e1 = e
assert str(e1) == 'Duplicate primary key found during insert'
assert type(e1).__name__ == 'ValueError'  

db.commit(tid)
db.close()
print ("COMMITT")
db = PersistentDB(schema, 'pk', overwrite=True)
















# first_tid = db.begin_transaction()
# db.insert_ts(first_tid, 1, ats1)
# row1 = DBRow.row_from_string(db._trees['pk'].get(1))
# assert(row1.pk == 1)
# assert(db._trees['pk'].has_key(1) == True)

# ROLLBACK
# db.rollback(first_tid)
# assert(db.tt == {})
# # Test that the set of keys is reverted
# assert(db._trees['pk'].has_key(1) == False)
# try:
#     row1 = DBRow.row_from_string(db._trees['pk'].get(1))
# except Exception as e: 
#     e1 = e
# assert str(e1) == ''
# assert type(e1).__name__ == 'KeyError'  