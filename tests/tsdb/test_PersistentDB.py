from tsdb import PersistentDB
from tsdb import DBRow
import timeseries as ts
import time
import unittest

#identity = lambda x: x

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

class TestPersistentDB(unittest.TestCase):
    
    # Tests
    def test_begin_transaction(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        assert(first_tid == 1)
        
        # Test that modifying this tid doesn't modify sequence
        first_tid += 1
        assert(first_tid == 2)
        
        second_tid = db.begin_transaction()
        assert(second_tid == 2)
        db.close()

    def test_commit(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        assert(first_tid == 1)
        db.insert_ts(first_tid, 1, ats1)
        db.commit(first_tid)
        db.close()

    def test_rollback(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        first_tid = db.begin_transaction()
        db.insert_ts(first_tid, 1, ats1)
        row1 = DBRow.row_from_string(db._trees['pk'].get(1))
        assert(row1.pk == 1)
        assert(db._trees['pk'].has_key(1) == True)

        # ROLLBACK
        db.rollback(first_tid)
        assert(db.tt == {})
        # Test that the set of keys is reverted
        assert(db._trees['pk'].has_key(1) == False)
        try:
            row1 = DBRow.row_from_string(db._trees['pk'].get(1))
        except Exception as e: 
            e1 = e
        assert str(e1) == ''
        assert type(e1).__name__ == 'KeyError'  
        db.close()

    def test_insert(self):
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

    def test_delete(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        tid = db.begin_transaction()

        db.insert_ts(tid, 1, ats1)
        db.insert_ts(tid, 2, ats1)
        db.insert_ts(tid, 3, ats1)
        db.insert_ts(tid, 4, ats1)

        # Upserting
        db.upsert_meta(tid, 1, {'blarg': 3, 'order': 1})
        db.upsert_meta(tid, 2, {'order': 1})
        db.upsert_meta(tid, 3, {'not_there': 3, 'order': 3})
        db.upsert_meta(tid, 4, {'blarg': 3})

        # Deleting
        db.delete_ts(tid, 1)
        db.delete_ts(tid, 2)
        db.delete_ts(tid, 3)

        # Tests
        pk_tree = db._trees['pk']
        assert(pk_tree.has_key(4) == True)
        assert(pk_tree.has_key(1) == False)

        # TODO!
        #assert(db.indexes['order'] == {})
        #assert(db.indexes['blarg'] == {3: {4}})
        # Check to ensure that PKs that have been deleted are no 
        # longer in the index
        #assert(db.indexes['pk'] == {4: {4}}) 
        db.close()

    def test_upsert(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        tid = db.begin_transaction()

        # INSERT
        db.insert_ts(tid, 1, ats1)
        db.insert_ts(tid, 2, ats1)

        # TEST
        pk_tree = db._trees['pk']
        base_node = pk_tree._follow(pk_tree._tree_ref)
        right_node = pk_tree._follow(base_node.right_ref)
        row1 = DBRow.row_from_string(pk_tree._follow(base_node.value_ref))
        row2 = DBRow.row_from_string(pk_tree._follow(right_node.value_ref))

        assert(row1.ts == ats1)
        assert(row2.ts == ats1)

        # UPSERT 
        # Don't allow TS upserts
        with self.assertRaises(ValueError):
            db.upsert_meta(tid, 2, {'ts': ats2})

        # Don't allow upserts for non-existant rows
        with self.assertRaises(ValueError):
            db.upsert_meta(tid, 3, {'not_there': 3, 'order': 1})

        # Upsert Metadata
        db.upsert_meta(tid, 2, {'not_there': 3, 'order': 1})

        # RETEST
        pk_tree = db._trees['pk']
        base_node = pk_tree._follow(pk_tree._tree_ref)
        right_node = pk_tree._follow(base_node.right_ref)
        more_right_node = pk_tree._follow(right_node.right_ref)
        row1 = DBRow.row_from_string(pk_tree._follow(base_node.value_ref))
        row2 = DBRow.row_from_string(pk_tree._follow(right_node.value_ref))

        assert(pk_tree.has_key(3) == False)

        assert(row1.ts == ats1)
        assert(row1.row['order'] == 0)
        assert(row2.ts == ats1)
        assert(row2.row['order'] == 1)
        db.close()

    def test_indexes(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        tid = db.begin_transaction()

        db.insert_ts(tid, '1', ats1)
        db.insert_ts(tid, '2', ats2)
        db.insert_ts(tid, '0', ats4)

        db.upsert_meta(tid, '2', {'order': 2, 'blarg':79})
        db.insert_ts(tid, '3', ats4)
        db.upsert_meta(tid, '3', {'not_there': 3, 'order': 1})

        assert(db._trees['pk'].get_all_keys() == ['1', '0', '2', '3'])

        assert(db._trees['order'].get(0) == ['1', '0'])
        assert(db._trees['order'].get(1) == ['3'])
        assert(db._trees['order'].get(2) == ['2'])

        assert(db._trees['blarg'].get(0) == ['1', '0', '3'])
        assert(db._trees['blarg'].get(79) == ['2'])
        db.close()

    def test_select_basic_operations(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        tid = db.begin_transaction()

        db.insert_ts(tid, 1, ats1)
        db.insert_ts(tid, 2, ats2)
        db.insert_ts(tid, 3, ats3)

        ids1, fields1 = db.select(tid, {'pk': {'==': 1}},None,None)
        assert(ids1 == [1])

        ids2, fields2 = db.select(tid, {'pk': {'>': 1}},None,None)
        assert(ids2 == [2, 3])

        ids3, fields3 = db.select(tid, {'pk': {'<': 2}},None,None)
        assert(ids3 == [1])

        ids4, fields4 = db.select(tid, {'pk': {'!=': 1}},None,None)
        assert(ids4 == [2, 3])

        ids5, fields5 = db.select(tid, {'pk': {'<=': 2}},None,None)
        assert(ids5 == [1, 2])

        ids6, fields6 = db.select(tid, {'pk': {'>=': 2}},None,None)
        assert(ids6 == [2, 3])

        ids7, fields7 = db.select(tid, {'pk': {'>': 1, '<': 3}}, None, None)
        assert(ids7 == [2])
        db.close()

    def test_select_basic_fields(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        tid = db.begin_transaction()

        db.insert_ts(tid, '1', ats1)
        db.insert_ts(tid, '2', ats2)
        db.insert_ts(tid, '3', ats3)

        db.upsert_meta(tid, '2', {'useless': 2, 'order': 2})

        # One result
        ids1, fields1 = db.select(tid, {'pk': {'==': '1'}}, ['ts'], None)
        assert(ids1 == ['1'])
        assert(fields1[0]['ts'] == ats1)

        # Two results
        ids2, fields2 = db.select(tid, {'pk': {'>': '1'}}, ['ts'], None)
        assert(len(ids2) == 2)
        assert('2' in ids2)
        assert('3' in ids2)
        assert(fields2[0]['ts'] == ats2)
        assert(fields2[1]['ts'] == ats3)

        # No results
        ids3, fields3 = db.select(tid, {'blarg': {'==': 1}}, ['ts'], None)
        assert(ids3 == [])

        # None Field List (just pks)
        ids4, fields4 = db.select(tid, {'pk': {'>': '0'}}, None, None)
        assert(len(ids4) == 3)
        assert(fields4 == [{}, {}, {}])

        # Empty Field List (everything but ts)
        ids5, fields5 = db.select(tid, {'pk': {'>': '0'}}, [], None)
        assert(len(ids5) == 3)
        assert(fields5[0]['pk'] in {'1','2','3'})
        assert(fields5[0]['mean'] == 0)
        #assert(fields5[1]['pk'] == '2')
        #assert(fields5[2]['pk'] == '3')

        # Named Field List (just that field) - since useless is not indexed, this will return everything
        ids6, fields6 = db.select(tid, {'useless': {'>': 0}}, ['useless'], None)
        assert(len(ids6) == 3)
        assert(fields6 == [{},{},{}])

        assert(db._trees['order'].get(2) == ['2'])

        # Named Field List (just that field)
        ids7, fields7 = db.select(tid, {'order': {'>': 0}}, ['order'], None)
        assert(ids7 == ['2'])
        assert(fields7 == [{'order': 2}])
        db.close()

    def test_select_basic_additional(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        tid = db.begin_transaction()

        db.insert_ts(tid, 1, ats1)
        db.insert_ts(tid, 2, ats2)
        db.insert_ts(tid, 3, ats3)

        db.upsert_meta(tid, 1, {'order': 1})
        db.upsert_meta(tid, 2, {'order': 3})
        db.upsert_meta(tid, 3, {'order': 5})

        # Limit to 2 results
        ids1, fields1 = db.select(tid, {'pk': {'>': 0}}, None, {'limit':2})
        assert(ids1 == [1, 2])

        # Useless Ascending
        ids2, fields2 = db.select(tid, {'pk': {'>': 0}}, None, {'sort_by':'+useless'})
        assert(ids2 == [1, 2, 3])

        # Order Ascending
        ids2, fields2 = db.select(tid, {'pk': {'>': 0}}, None, {'sort_by':'+order'})
        assert(ids2 == [1, 2, 3])

        # Order Descending
        ids3, fields3 = db.select(tid, {'pk': {'>': 0}}, None, {'sort_by':'-order'})
        assert(ids3 == [3, 2, 1])
        db.close()

    def test_complex(self):
        db = PersistentDB(schema, 'pk', overwrite=True)
        tid = db.begin_transaction()

        for i in range(100):
            db.insert_ts(tid, i, ats1)
            db.upsert_meta(tid, i, {'blarg': i})
            db.upsert_meta(tid, i, {'order': -i})

        ids1, fields1 = db.select(tid, {'pk': {'>': 10, '<=' : 50}},None,{'limit':10,'sort_by':'-blarg'})
        assert(ids1 == [50, 49, 48, 47, 46, 45, 44, 43, 42, 41])

        ids2, fields2 = db.select(tid, meta={}, fields=[], additional={'limit':15,'sort_by': '-order'})
        assert(ids2 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        db.close()