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
  'pk': {'convert': identity, 'index': None, 'default': -1},  # Will be indexed anyways
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

class TestTransactions(unittest.TestCase):
    
    # Tests
    def test_transact1(self):
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

        db.rollback(second_tid)

        third_tid = db.begin_transaction()
        ids1, fields1 = db.select(third_tid, {'pk': {'==': 1}}, ['ts', 'order'], None)
        assert(ids1 == [1])
        assert(fields1[0]['ts'] == ats1)
        assert(fields1[0]['order'] == 0.0)

        db.close()

    def test_closing(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, 1, ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get(1))
        assert(row1.pk == 1)
        assert(db._trees['pk'].has_key(1) == True)

        #COMMIT 
        db.commit(first_tid)

        db.close()

        db2 = PersistentDB(schema, 'pk', overwrite=False)


        second_tid = db2.begin_transaction()
        ids1, fields1 = db2.select(second_tid, {'pk': {'==': 1}}, ['ts', 'order'], None)
        print (fields1)
        assert(ids1 == [1])
        assert(fields1[0]['ts'] == ats1)
        assert(fields1[0]['order'] == 0.0)

        db2.close()

    def test_close_commit(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, 1, ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get(1))
        assert(row1.pk == 1)
        assert(db._trees['pk'].has_key(1) == True)

        db.close()


        #COMMIT 
        try:
            db.commit(first_tid)
        except Exception as e: 
            e1 = e
        assert type(e1).__name__ == 'ValueError'  

    def test_different_schemas(self):

        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, 1, ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get(1))
        assert(row1.pk == 1)
        assert(db._trees['pk'].has_key(1) == True)

        db.close()
        e1 = ''
        try:
            db2 = PersistentDB(schema2, 'pk', overwrite=False)
            db2.close()
        except Exception as e: 
            e1 = e
        assert type(e1).__name__ == 'ValueError'  





