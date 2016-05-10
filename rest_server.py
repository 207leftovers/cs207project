#!/usr/bin/env python3
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
  'sig_epsilon_estimate': {'convert': float, 'index': 1},
  'sig_eta_estimate': {'convert': float, 'index': 1},
  'prediction': {'convert': identity, 'index': None}
}

NUMVPS = 5


#TEST this out by running
#curl http://localhost:9999/ -X POST -d "pk=four&op=insert_ts&ts=[[0.0, 1.0, 4.0], [0.0, 0.0, 4.0]]" 

def main():
    # we augment the schema by adding columns for 5 vantage points
    for i in range(NUMVPS):
        schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1}
    db = DictDB(schema, 'pk')
    server = TSDBServer(db)
    server.rest_run()

if __name__=='__main__':
    main()