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

    async def insert_ts(self, primary_key, ts):
        # your code here, construct from the code in tsdb_ops.py
        InsertedTS = TSDBOp_InsertTS(primary_key, ts)
        return await self._send(InsertedTS.to_json())

    async def delete_ts(self, primary_key):
        delete_ts_op = TSDBOp_DeleteTS(primary_key)
        return await self._send(delete_ts_op.to_json())
    
    async def upsert_meta(self, primary_key, metadata_dict):
        # your code here
        upserted_meta = TSDBOp_UpsertMeta(primary_key, metadata_dict)
        return await self._send(upserted_meta.to_json())

    async def select(self, metadata_dict={}, fields=None, additional=None):
        # your code here
        select_op = TSDBOp_Select(metadata_dict, fields, additional)
        return await self._send(select_op.to_json())

    async def augmented_select(self, proc, target, arg=None, metadata_dict={}, additional=None):
        #your code here
        aug_select_op = TSDBOp_AugmentedSelect(proc, target, arg, md, additional)
        return await self._send(aug_select_op.to_json())

    async def add_trigger(self, proc, onwhat, target, arg):
        # your code here
        add_trigger_op = TSDBOp_AddTrigger(proc, onwhat, target, arg)
        return await self._send(add_trigger_op.to_json())

    async def remove_trigger(self, proc, onwhat):
        # your code here
        remove_trigger_op = TSDBOp_RemoveTrigger(proc, onwhat)
        return await self._send(remove_trigger_op.to_json())

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload

    async def _run(self, msg):
        with aiohttp.ClientSession() as session:
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


        # loop = asyncio.get_event_loop()  
        # coro = asyncio.ensure_future(self._run(msg))
        # loop.run_until_complete(coro)  
        # return coro.result()

        loop = asyncio.get_event_loop()
        status, payload_str = await self._run(msg)
        # print (payload_str)
        payload_dict = json.loads(payload_str, object_pairs_hook=OrderedDict)
        status = payload_dict['status']
        payload = payload_dict['payload']
        # print ("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        # print (status)
        # print (payload)
        return status, payload