#!/usr/bin/env python3
from tsdb import TSDBServer, PersistentDB
import timeseries as ts

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

#TEST this out by running

#Begin transaction
#curl -H "Content-Type: application/json" -X POST -d '{"op":"begin_transaction"}' http://localhost:9999/

#insert TS
#curl -H "Content-Type: application/json" -X POST -d '{"op":"insert_ts","tid":2,"ts":[[1.0, 2.0, 3.0, 2.0, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0]], "pk":1}' http://localhost:9999/

# {"op": "begin_transaction"}
# C> status: 200
# C> payload {"op": "begin_transaction", "status": 0, "payload": 1}
# {"arg": null, "op": "add_trigger", "proc": "stats", "tid": 1, "onwhat": "insert_ts", "target": ["mean", "std"]}
# C> status: 200
# C> payload {"op": "add_trigger", "status": 0, "payload": null}
# PRIMARY KEY 1 <class 'str'>
# {"pk": "1", "ts": [[1.0, 2.0, 3.0, 2.0, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0]], "op": "insert_ts", "tid": 1}
# C> status: 200
# C> payload {"op": "insert_ts", "status": 0, "payload": null}
# {"additional": null, "md": {"pk": {"==": "1"}}, "fields": ["ts", "mean", "std"], "op": "select", "tid": 1}
# C> status: 200
# C> payload {"op": "select", "status": 0, "payload": {"1": {"mean": 2.0, "ts": [[0.0, 4.0, 1.0, 3.0, 2.0], [1.0, 1.0, 2.0, 2.0, 3.0]], "std": 1.4142135623730951}}}
# {"pk": "1", "md": {"order": 1}, "op": "upsert_meta", "tid": 1}
# C> status: 200
# C> payload {"op": "upsert_meta", "status": 0, "payload": null}
# {"additional": null, "md": {"order": {"==": 1}}, "fields": ["pk", "order"], "op": "select", "tid": 1}
# C> status: 200
# C> payload {"op": "select", "status": 0, "payload": {"1": {"pk": "1", "order": 1}}}
# {"onwhat": "insert_ts", "proc": "stats", "op": "remove_trigger", "tid": 1}
# C> status: 200
# C> payload {"op": "remove_trigger", "status": 0, "payload": null}
# PRIMARY KEY 2 <class 'str'>
# {"pk": "2", "ts": [[1.0, 2.0, 3.0, 2.0, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0]], "op": "insert_ts", "tid": 1}
# C> status: 200
# C> payload {"op": "insert_ts", "status": 0, "payload": null}
# {"additional": null, "md": {"pk": {"==": "2"}}, "fields": ["ts", "mean", "std"], "op": "select", "tid": 1}
# C> status: 200
# C> payload {"op": "select", "status": 0, "payload": {"2": {"mean": 0.0, "ts": [[0.0, 4.0, 1.0, 3.0, 2.0], [1.0, 1.0, 2.0, 2.0, 3.0]], "std": 0.0}}}
# {"pk": "1", "op": "delete_ts", "tid": 1}
# C> status: 200
# C> payload {"op": "delete_ts", "status": 0, "payload": null}
# {"additional": null, "md": {"pk": {"==": "1"}}, "fields": ["ts", "mean", "std"], "op": "select", "tid": 1}
# C> status: 200
# C> payload {"op": "select", "status": 0, "payload": {}}

#
def main():
    db = PersistentDB(schema, 'pk', overwrite=True)
    server = TSDBServer(db)
    server.rest_run()

if __name__=='__main__':
    main()