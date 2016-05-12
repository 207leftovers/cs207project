import asyncio
from .tsdb_serialization import serialize, LENGTH_FIELD_LENGTH, Deserializer
from .tsdb_ops import *
from .tsdb_error import *
import aiohttp
import json
from collections import OrderedDict

class TSDB_REST_Client(object):
    """
    The client. This could be used in a python program, web server, or REPL!
    """
    def __init__(self, port=9999):
        self.port = port
        self.url = "http://localhost:"+str(port)+"/"
    
    async def begin_transaction(self):
        begin_tx = TSDBOp_BeginTransaction()
        return await self._send(begin_tx.to_json())    
    
    async def commit(self, tid):
        commit_op = TSDBOp_Commit(tid)
        return await self._send(commit_op.to_json()) 
    
    async def rollback(self, tid):
        rollback_op = TSDBOp_Rollback(tid)
        return await self._send(rollback_op.to_json()) 
        
    async def insert_ts(self, tid, primary_key, ts):
        # your code here, construct from the code in tsdb_ops.py
        print ("PRIMARY KEY", primary_key, type(primary_key))
        InsertedTS = TSDBOp_InsertTS(tid, primary_key, ts)
        return await self._send(InsertedTS.to_json())

    async def delete_ts(self, tid, primary_key):
        delete_ts_op = TSDBOp_DeleteTS(tid, primary_key)
        return await self._send(delete_ts_op.to_json())
    
    async def upsert_meta(self, tid, primary_key, metadata_dict):
        upserted_meta = TSDBOp_UpsertMeta(tid, primary_key, metadata_dict)
        return await self._send(upserted_meta.to_json())

    async def select(self, tid, metadata_dict={}, fields=None, additional=None):
        select_op = TSDBOp_Select(tid, metadata_dict, fields, additional)
        return await self._send(select_op.to_json())

    async def augmented_select(self, tid, proc, target, arg=None, metadata_dict={}, additional=None):
        aug_select_op = TSDBOp_AugmentedSelect(tid, proc, target, arg, md, additional)
        return await self._send(aug_select_op.to_json())

    async def add_trigger(self, tid, proc, onwhat, target, arg):
        add_trigger_op = TSDBOp_AddTrigger(tid, proc, onwhat, target, arg)
        return await self._send(add_trigger_op.to_json())

    async def remove_trigger(self, tid, proc, onwhat):
        remove_trigger_op = TSDBOp_RemoveTrigger(tid, proc, onwhat)
        return await self._send(remove_trigger_op.to_json())

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload
    async def _run(self, msg):
        with aiohttp.ClientSession() as session:
            print (json.dumps(msg))
            async with session.post(self.url, data=json.dumps(msg)) as resp:
                #print(await resp.text())
                status = resp.status
                payload = await resp.text()

                print ("C> status:", status)
                print ("C> payload", payload)
                return status, payload

    #call `_send` with a well formed message to send.
    #once again replace this function if appropriate
    async def _send(self, msg):
        loop = asyncio.get_event_loop()
        status, payload_str = await self._run(msg)
        payload_dict = json.loads(payload_str, object_pairs_hook=OrderedDict)
        status = payload_dict['status']
        payload = payload_dict['payload']
        return status, payload