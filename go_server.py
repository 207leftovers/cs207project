#!/usr/bin/env python3
from tsdb import TSDBServer, PersistentDB
import timeseries as ts

#identity = lambda x: x

schema = {
  'pk': {'convert': str, 'index': None, 'default': -1},  # Will be indexed anyways
  'ts': {'convert': str, 'index': None, 'default': None},
  'order': {'convert': int, 'index': 1, 'default': 0},
  'blarg': {'convert': int, 'index': 1, 'default': 0},
  'useless': {'convert': str, 'index': None, 'default': 0}, # This will be ignored becuase there is no index
  'mean': {'convert': float, 'index': 1, 'default': 0.0},
  'std': {'convert': float, 'index': 1, 'default': 0.0},
  'sig_epsilon_estimate': {'convert': float, 'index': 1, 'default': 0.0},
  'sig_eta_estimate': {'convert': float, 'index': 1, 'default': 0.0},
  'prediction': {'convert': str, 'index': None, 'default': None}
}

def main():
    db = PersistentDB(schema, 'pk', overwrite=False)
    server = TSDBServer(db)
    server.run()

if __name__=='__main__':
    main()