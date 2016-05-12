#!/usr/bin/env python3
from tsdb import TSDBServer, PersistentDB
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
  'sig_epsilon_estimate': {'convert': float, 'index': 1, 'default': 0.0},
  'sig_eta_estimate': {'convert': float, 'index': 1, 'default': 0.0},
  'prediction': {'convert': identity, 'index': None, 'default': None}
}

#TEST this out by running
#curl -H "Content-Type: application/json" -X POST -d '{"op":"begin_transaction"}' http://localhost:9999/
#curl -H "Content-Type: application/json" -X POST -d '{"op":"insert_ts","tid":2,"ts":[[1.0, 2.0, 3.0, 2.0, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0]], "pk":1}' http://localhost:9999/

def main():
    db = PersistentDB(schema, 'pk', overwrite=True)
    server = TSDBServer(db)
    server.rest_run()

if __name__=='__main__':
    main()