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
    
# Tests
def test_begin_transaction():
    db = PersistentDB(schema, 'pk', overwrite=True)
    first_tid = db.begin_transaction()
    assert(first_tid == 1)
    
    # Test that modifying this tid doesn't modify sequence
    first_tid += 1
    assert(first_tid == 2)
    
    second_tid = db.begin_transaction()
    assert(second_tid == 2)
    
def test_commit():
    db = PersistentDB(schema, 'pk', overwrite=True)
    first_tid = db.begin_transaction()
    assert(first_tid == 1)
    db.insert_ts(first_tid, 1, ats1)
    db.commit(first_tid)
    
def test_rollback():
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

    
def test_insert():
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
    
def test_delete():
    #time.sleep(1)
    db = PersistentDB(schema, 'pk', overwrite=True)
    tid = db.begin_transaction()
    
    # Upserting
    db.upsert_meta(tid, 1, {'ts': ats1, 'blarg': 3, 'order': 1})
    db.upsert_meta(tid, 2, {'ts': ats1, 'order': 1})
    db.upsert_meta(tid, 3, {'ts': ats1, 'not_there': 3, 'order': 3})
    db.upsert_meta(tid, 4, {'ts': ats1, 'blarg': 3})
    
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
    
def test_upsert():
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
    db.upsert_meta(tid, 2, {'ts': ats2})
    db.upsert_meta(tid, 3, {'ts': ats4, 'not_there': 3, 'order': 1})
    
    # RETEST
    pk_tree = db._trees['pk']
    base_node = pk_tree._follow(pk_tree._tree_ref)
    right_node = pk_tree._follow(base_node.right_ref)
    more_right_node = pk_tree._follow(right_node.right_ref)
    row1 = DBRow.row_from_string(pk_tree._follow(base_node.value_ref))
    row2 = DBRow.row_from_string(pk_tree._follow(right_node.value_ref))
    row3 = DBRow.row_from_string(pk_tree._follow(more_right_node.value_ref))
    
    assert(row1.ts == ats1)
    assert(row1.row['order'] == 0)
    assert(row2.ts == ats2)
    assert(row3.ts == ats4)
    assert(row3.row['order'] == 1)

def a_test_select_basic_operations():
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
    
    ids7, fields7 = db.select(tid, {'pk': {'>': 1, '<': 3}},None,None)
    assert(ids7 == [2])

def a_test_select_basic_fields():
    db = PersistentDB(schema, 'pk', overwrite=True)
    tid = db.begin_transaction()
    
    db.insert_ts(tid, 1, ats1)
    db.insert_ts(tid, 2, ats2)
    db.insert_ts(tid, 3, ats3)
    
    db.upsert_meta(tid, 2, {'useless': 2})
    
    # One result
    ids1, fields1 = db.select(tid, {'pk': {'==': 1}},['ts'],None)
    assert(ids1 == [1])
    assert(fields1[0]['ts'] == ats1)
    
    # Two results
    ids2, fields2 = db.select(tid, {'pk': {'>': 1}},['ts'],None)
    assert(ids2 == [2,3])
    assert(fields2[0]['ts'] == ats2)
    assert(fields2[1]['ts'] == ats3)
    
    # No results
    ids3, fields3 = db.select(tid, {'blarg': {'=': 1}},['ts'],None)
    assert(ids3 == [])
    
    # None Field List (just pks)
    ids4, fields4 = db.select(tid, {'pk':{'>': 0}},None,None)
    assert(ids4 == [1, 2, 3])
    assert(fields4 == [{}, {}, {}])
    
    # Empty Field List (everything but ts)
    ids5, fields5 = db.select(tid, {'pk':{'>': 0}},[],None)
    assert(ids5 == [1, 2, 3])
    assert(fields5 == [{'pk': 1}, {'pk': 2, 'useless': 2}, {'pk': 3}])
    
    # Named Field List (just that field)
    ids6, fields6 = db.select(tid, {'useless':{'>': 0}},['useless'],None)
    assert(ids6 == [2])
    assert(fields6 == [{'useless': 2}])
    
def a_test_select_basic_additional():
    db = PersistentDB(schema, 'pk', overwrite=True)
    tid = db.begin_transaction()
    
    db.insert_ts(tid, 1, ats1)
    db.insert_ts(tid, 2, ats2)
    db.insert_ts(tid, 3, ats3)
    
    db.upsert_meta(tid, 1, {'useless': 1})
    db.upsert_meta(tid, 2, {'useless': 3})
    db.upsert_meta(tid, 3, {'useless': 5})
    
    # Limit to 2 results
    ids1, fields1 = db.select(tid, {'pk': {'>': 0}},None,{'limit':2})
    assert(ids1 == [1, 2])
    
    # Order Ascending
    ids2, fields2 = db.select(tid, {'pk': {'>': 0}},None,{'sort_by':'+useless'})
    assert(ids2 == [1, 2, 3])
    
    # Order Descending
    ids3, fields3 = db.select(tid, {'pk': {'>': 0}},None,{'sort_by':'-useless'})
    assert(ids3 == [3, 2, 1])
    
def a_test_complex():
    db = PersistentDB(schema, 'pk', overwrite=True)
    tid = db.begin_transaction()
    
    for i in range(100):
        db.insert_ts(tid, i, ats1)
        db.upsert_meta(tid, i, {'useless': i})
        db.upsert_meta(tid, i, {'order': -i})

    ids1, fields1 = db.select(tid, {'pk': {'>': 10, '<=' : 50}},None,{'limit':10,'sort_by':'-useless'})
    assert(ids1 == [50, 49, 48, 47, 46, 45, 44, 43, 42, 41])
    
    ids2, fields2 = db.select(tid, meta={}, fields=[], additional={'limit':15,'sort_by': '-order'})
    assert(ids2 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])