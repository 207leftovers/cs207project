from tsdb import DictDB
import timeseries as ts

identity = lambda x: x

schema = {
  'pk': {'convert': identity, 'index': None},  #will be indexed anyways
  'ts': {'convert': identity, 'index': None},
  'order': {'convert': int, 'index': 1},
  'blarg': {'convert': int, 'index': 1},
  'useless': {'convert': identity, 'index': 1},
  'mean': {'convert': float, 'index': 1},
  'std': {'convert': float, 'index': 1},
  'vp': {'convert': bool, 'index': 1}
}

NUMVPS = 5

# we augment the schema by adding columns for 5 vantage points
for i in range(NUMVPS):
    schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}

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
    
# Tests
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
    
    db.insert_ts(1, ats1)
    db.insert_ts(2, ats1)
    
    db.upsert_meta(2, {'ts': ats2})
    db.upsert_meta(3, {'ts': ats2, 'not_there': 3, 'order': 1})
    
    rows = db.rows
    
    assert(rows[1]['ts'] == ats1)
    assert(rows[2]['ts'] == ats2)
    assert(rows[3]['ts'] == ats2)
    assert(rows[3]['order'] == 1)
    
def test_delete():
    db = DictDB(schema, 'pk')

    # Upserting
    db.upsert_meta(1, {'ts': ats1, 'blarg': 3, 'order': 1})
    db.upsert_meta(2, {'ts': ats1, 'order': 1})
    db.upsert_meta(3, {'ts': ats1, 'not_there': 3, 'order': 3})
    db.upsert_meta(4, {'ts': ats1, 'blarg': 3})
    
    # Deleting
    db.delete_ts(1)
    db.delete_ts(2)
    db.delete_ts(3)
    
    # Tests
    rows = db.rows
    assert(len(rows) == 1)
    assert(4 in rows)
    assert(1 not in rows)
    assert(db.indexes['order'] == {})
    assert(db.indexes['blarg'] == {3: {4}})
    print(db.indexes)
    assert(db.indexes['pk'] == {4: {4}})
    
def test_select_basic_operations():
    db = DictDB(schema, 'pk')
    
    db.insert_ts(1, ats1)
    
    db.insert_ts(2, ats2)
    db.insert_ts(3, ats3)
    
    ids1, fields1 = db.select({'pk': {'==': 1}},None,None)
    assert(ids1 == [1])

    ids2, fields2 = db.select({'pk': {'>': 1}},None,None)
    assert(ids2 == [2, 3])
    
    ids3, fields3 = db.select({'pk': {'<': 2}},None,None)
    assert(ids3 == [1])
    
    ids4, fields4 = db.select({'pk': {'!=': 1}},None,None)
    assert(ids4 == [2, 3])
    
    ids5, fields5 = db.select({'pk': {'<=': 2}},None,None)
    assert(ids5 == [1, 2])
    
    ids6, fields6 = db.select({'pk': {'>=': 2}},None,None)
    assert(ids6 == [2, 3])
    
    ids7, fields7 = db.select({'pk': {'>': 1, '<': 3}},None,None)
    assert(ids7 == [2])

def test_select_basic_fields():
    db = DictDB(schema, 'pk')
    
    db.insert_ts(1, ats1)
    db.insert_ts(2, ats2)
    db.insert_ts(3, ats3)
    
    db.upsert_meta(2, {'useless': 2})
    
    # One result
    ids1, fields1 = db.select({'pk': {'==': 1}},['ts'],None)
    assert(ids1 == [1])
    assert(fields1[0]['ts'] == ats1)
    
    # Two results
    ids2, fields2 = db.select({'pk': {'>': 1}},['ts'],None)
    assert(ids2 == [2,3])
    assert(fields2[0]['ts'] == ats2)
    assert(fields2[1]['ts'] == ats3)
    
    # No results
    ids3, fields3 = db.select({'blarg': {'=': 1}},['ts'],None)
    assert(ids3 == [])
    
    # None Field List (just pks)
    ids4, fields4 = db.select({'pk':{'>': 0}},None,None)
    assert(ids4 == [1, 2, 3])
    assert(fields4 == [{}, {}, {}])
    
    # Empty Field List (everything but ts)
    ids5, fields5 = db.select({'pk':{'>': 0}},[],None)
    assert(ids5 == [1, 2, 3])
    assert(fields5 == [{'pk': 1}, {'pk': 2, 'useless': 2}, {'pk': 3}])
    
    # Named Field List (just that field)
    ids6, fields6 = db.select({'useless':{'>': 0}},['useless'],None)
    assert(ids6 == [2])
    assert(fields6 == [{'useless': 2}])
    
def test_select_basic_additional():
    db = DictDB(schema, 'pk')
    
    db.insert_ts(1, ats1)
    db.insert_ts(2, ats2)
    db.insert_ts(3, ats3)
    
    db.upsert_meta(1, {'useless': 1})
    db.upsert_meta(2, {'useless': 3})
    db.upsert_meta(3, {'useless': 5})
    
    # Limit to 2 results
    ids1, fields1 = db.select({'pk': {'>': 0}},None,{'limit':2})
    assert(ids1 == [1, 2])
    
    # Order Ascending
    ids2, fields2 = db.select({'pk': {'>': 0}},None,{'sort_by':'+useless'})
    assert(ids2 == [1, 2, 3])
    
    # Order Descending
    ids3, fields3 = db.select({'pk': {'>': 0}},None,{'sort_by':'-useless'})
    assert(ids3 == [3, 2, 1])
    
def test_complex():
    db = DictDB(schema, 'pk')
    
    for i in range(100):
        db.insert_ts(i, ats1)
        db.upsert_meta(i, {'useless': i})
        db.upsert_meta(i, {'order': -i})

    ids1, fields1 = db.select({'pk': {'>': 10, '<=' : 50}},None,{'limit':10,'sort_by':'-useless'})
    assert(ids1 == [50, 49, 48, 47, 46, 45, 44, 43, 42, 41])
    
    ids2, fields2 = db.select(meta={}, fields=[], additional={'limit':15,'sort_by': '-order'})
    assert(ids2 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])