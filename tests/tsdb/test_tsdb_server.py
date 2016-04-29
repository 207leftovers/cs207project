from tsdb import TSDBServer, DictDB
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

#def test_insert():
    #db = DictDB(schema, 'pk')
    #server = TSDBServer(db)
    #server.run()
    
    #t = [0,1,2,3,4]
    #v = [1.0,2.0,3.0,2.0,1.0]
    #ats = ts.TimeSeries(t, v)
    
    #op = {}
    #op['pk'] = 1
    #op['ts'] = ats
    #server.loop.stop()    
    #server._insert_ts(op)
    #assert(1 == 2)
