#Begin transaction
echo Starting Transaction
echo curl -H "Content-Type: application/json" -X POST -d '{"op":"begin_transaction"}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d '{"op":"begin_transaction"}' http://localhost:9999/
echo
echo 

#Add Trigger
echo Adding Trigger
echo curl -H "Content-Type: application/json" -X POST -d '{"arg": null, "op": "add_trigger", "proc": "stats", "tid": 1, "onwhat": "insert_ts", "target": ["mean", "std"]}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d '{"arg": null, "op": "add_trigger", "proc": "stats", "tid": 1, "onwhat": "insert_ts", "target": ["mean", "std"]}' http://localhost:9999/
echo
echo

#insert TS
echo Inserting TS
echo curl -H "Content-Type: application/json" -X POST -d '{"op":"insert_ts","tid":1,"ts":[[1.0, 2.0, 3.0, 2.0, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0]], "pk":1}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d '{"op":"insert_ts","tid":1,"ts":[[1.0, 2.0, 3.0, 2.0, 1.0], [0.0, 1.0, 2.0, 3.0, 4.0]], "pk":1}' http://localhost:9999/
echo
echo


#Select
echo Selecting trigger fields
echo curl -H "Content-Type: application/json" -X POST -d '{"additional": null, "md": {"pk": {"==": "1"}}, "fields": ["ts", "mean", "std"], "op": "select", "tid": 1}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d '{"additional": null, "md": {"pk": {"==": "1"}}, "fields": ["ts", "mean", "std"], "op": "select", "tid": 1}' http://localhost:9999/
echo
echo

echo Upserting Meta
echo curl -H "Content-Type: application/json" -X POST -d '{"pk": "1", "md": {"order": 1}, "op": "upsert_meta", "tid": 1}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d '{"pk": "1", "md": {"order": 1}, "op": "upsert_meta", "tid": 1}' http://localhost:9999/
echo
echo

#Selecting Upserts
echo Selecting Upserts
echo curl -H "Content-Type: application/json" -X POST -d ' {"additional": null, "md": {"order": {"==": 1}}, "fields": ["pk", "order"], "op": "select", "tid": 1}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d ' {"additional": null, "md": {"order": {"==": 1}}, "fields": ["pk", "order"], "op": "select", "tid": 1}' http://localhost:9999
echo 
echo

#Deleting TS
echo Deleting TS
echo curl -H "Content-Type: application/json" -X POST -d '{"pk": "1", "op": "delete_ts", "tid": 1}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d '{"pk": "1", "op": "delete_ts", "tid": 1}' http://localhost:9999
echo 
echo

#Checking deletes
echo Checking Deletes
echo curl -H "Content-Type: application/json" -X POST -d ' {"additional": null, "md": {"order": {"==": 1}}, "fields": ["pk", "order"], "op": "select", "tid": 1}' http://localhost:9999/
curl -H "Content-Type: application/json" -X POST -d ' {"additional": null, "md": {"order": {"==": 1}}, "fields": ["pk", "order"], "op": "select", "tid": 1}' http://localhost:9999
echo 
echo