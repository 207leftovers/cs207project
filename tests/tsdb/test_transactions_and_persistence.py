from tsdb import PersistentDB
from tsdb import DBRow
import timeseries as ts
import time
import unittest

schema = {
  'pk': {'convert': str, 'index': None, 'default': -1},  # Will be indexed anyways
  'ts': {'convert': str, 'index': None, 'default': None},
  'order': {'convert': int, 'index': 1, 'default': 0},
  'blarg': {'convert': int, 'index': 1, 'default': 0},
  'useless': {'convert': str, 'index': None, 'default': 0},
  'mean': {'convert': float, 'index': 1, 'default': 0},
  'std': {'convert': float, 'index': 1, 'default': 0},
  'vp': {'convert': bool, 'index': 1, 'default': False}
}

schema2 = {
  'pk': {'convert': str, 'index': None, 'default': -1}
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
    def test_transact(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, '1', ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get("1"))
        assert(row1.pk == "1")
        assert(db._trees['pk'].has_key("1") == True)

        # Commit 
        db.commit(first_tid)
        
        # Rollback with no open transaction
        with self.assertRaises(ValueError):
            db.rollback(first_tid)

        # Add Meta Data
        second_tid = db.begin_transaction()
        _, fields1 = db.select(second_tid, {'pk': {'==': '1'}}, ['ts', 'order'], None)
        assert(fields1[0]['order'] == 0)

        # Upsert with a new value for ORDER
        db.upsert_meta(second_tid, '1', { 'order': 5})
        ids1, fields1 = db.select(second_tid, {'pk': {'==': '1'}}, ['ts', 'order'], None)
        assert(ids1 == ['1'])
        assert(fields1[0]['ts'] == ats1)
        assert(fields1[0]['order'] == 5)
        assert(db._trees['pk'].get_as_row('1').row['order'] == 5)

        # Rollback
        db.rollback(second_tid)

        # Test that values are still what they were after the first commit
        third_tid = db.begin_transaction()
        ids1, fields1 = db.select(third_tid, {'pk': {'==': '1'}}, ['ts', 'order'], None)
        assert(ids1 == ['1'])
        assert(fields1[0]['ts'] == ats1)
        
        # Check the trees
        assert(db._trees['pk'].get_as_row('1').row['order'] == 0)
        #assert(db._trees['order'].get(5) == ['1'])
        assert(fields1[0]['order'] == 0.0)

        db.close()

    def test_closing(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, 1, ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get("1"))
        assert(row1.pk == "1")
        assert(db._trees['pk'].has_key("1") == True)

        #COMMIT 
        db.commit(first_tid)
        db.close()

        try:
            db2 = PersistentDB(schema, 'pk', overwrite=False)
        except Exception as e:
            assert(e == None)

        second_tid = db2.begin_transaction()
        ids1, fields1 = db2.select(second_tid, {'pk': {'==': '1'}}, ['ts', 'order'], None)
        print (fields1)
        assert(ids1 == ["1"])
        assert(fields1[0]['ts'] == ats1)
        assert(fields1[0]['order'] == 0.0)
        db2.close()

    def test_close_commit(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, '1', ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get("1"))
        assert(row1.pk == "1")
        assert(db._trees['pk'].has_key("1") == True)
        db.close()

        #COMMIT 
        try:
            db.commit(first_tid)
        except Exception as e: 
            e1 = e
        assert type(e1).__name__ == 'ValueError'  

class TestPersistence(unittest.TestCase):
    def test_different_schemas(self):
        db = PersistentDB(schema, 'pk', f='2', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, 1, ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get("1"))
        assert(row1.pk == "1")
        assert(db._trees['pk'].has_key("1") == True)
        db.close()
        
        e1 = ''
        try:
            db2 = PersistentDB(schema2, 'pk', f='2', overwrite=False)
            db2.close()
        except Exception as e: 
            e1 = e
        assert type(e1).__name__ == 'ValueError'  
        
        db3 = PersistentDB(schema, 'pk', f='2', overwrite=False)
        db3.close()

    def test_vp_schema(self):
        print(schema.copy())
        db = PersistentDB(schema.copy(), 'pk', f='3', overwrite=True)
        tid = db.begin_transaction()
        db.insert_ts(tid, 1, ats1)
        db.create_vp(tid, 1)
        db.close()
        
        # Checks to ensure there was no vp added
        db2 = PersistentDB(schema.copy(), 'pk', f='3', overwrite=False)
        tid = db2.begin_transaction()
        db2.insert_ts(tid, 1, ats1)
        db2.create_vp(tid, 1)
        db2.commit(tid)
        db2.close()
        
        with self.assertRaises(ValueError):
            db3 = PersistentDB(schema.copy(), 'pk', f='3', overwrite=False)
            db3.close()
