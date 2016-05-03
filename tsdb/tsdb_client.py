import asyncio
from .tsdb_serialization import serialize, LENGTH_FIELD_LENGTH, Deserializer
from .tsdb_ops import *
from .tsdb_error import *

class TSDBClient(object):
    """
    The client. This could be used in a python program, web server, or REPL!
    """
    def __init__(self, port=9999):
        self.port = port

    async def insert_ts(self, primary_key, ts):
        # your code here, construct from the code in tsdb_ops.py
        #times = ts.times()
        #values = ts.values()
        #times =  map(str, times)
        #values =  map(str, values)
        #ts_dict = dict(zip(times, values))
        InsertedTS = TSDBOp_InsertTS(primary_key, ts)
        return await self._send(InsertedTS.to_json())

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

    async def _send_coro(self, msg, loop):
        # your code here
        print ("C> sending:", msg)
        serialized_msg = serialize(msg)

        reader, writer = await asyncio.open_connection('127.0.0.1', self.port, loop = loop)

        writer.write(serialized_msg)
        await writer.drain()

        data = await reader.read()
        #print('Received: %r' % data)
        writer.close()

        deserializer = Deserializer();
        deserializer.append(data)
        if deserializer.ready():
            response = deserializer.deserialize()
            status = response['status']
            payload = response['payload']

            print ("C> status:", status)
            print ("C> payload", payload)
            return status, payload
        else:
            raise(ValueError("tsdb_client never received full json"))

    # Call `_send` with a well formed message to send.
    # Once again replace this function if appropriate
    async def _send(self, msg):
        loop = asyncio.get_event_loop()
        # These lines don't work
        #coro = asyncio.ensure_future(self._send_coro(msg, loop))
        #loop.run_until_complete(coro)
        status, payload = await self._send_coro(msg, loop)
        return status, payload