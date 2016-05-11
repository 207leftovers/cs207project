#!/usr/bin/env python3
from tsdb import TSDBServer, DictDB
import timeseries as ts

identity = lambda x: x

schema = {
  'pk': {'convert': identity, 'index': None, 'default': -1},  # Will be indexed anyways
  'ts': {'convert': identity, 'index': None, 'default': None},
  'order': {'convert': int, 'index': 1, 'default': 0},
  'blarg': {'convert': int, 'index': 1, 'default': 0},
  'useless': {'convert': identity, 'index': None, 'default': 0}, # This will be ignored becuase there is no index
  'mean': {'convert': float, 'index': 1, 'default': 0.0},
  'std': {'convert': float, 'index': 1, 'default': 0.0},
  'vp': {'convert': bool, 'index': 1, 'default': False}
  'sig_epsilon_estimate': {'convert': float, 'index': 1, 'default': 0.0},
  'sig_eta_estimate': {'convert': float, 'index': 1, 'default': 0.0},
  'prediction': {'convert': identity, 'index': None, 'default': None}
}

NUMVPS = 5

def main():
    # we augment the schema by adding columns for 5 vantage points
    for i in range(NUMVPS):
        schema["d_vp-{}".format(i)] = {'convert': float, 'index': 1, 'default': 0.0}
    db = PersistentDB(schema, 'pk')
    server = TSDBServer(db)
    server.run()

if __name__=='__main__':
    main()