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

    def insert_ts(self, primary_key, ts):
        # your code here, construct from the code in tsdb_ops.py
        #times = ts.times()
        #values = ts.values()
        #times =  map(str, times)
        #values =  map(str, values)
        #ts_dict = dict(zip(times, values))
        InsertedTS = TSDBOp_InsertTS(primary_key, ts)
        return self._send(InsertedTS.to_json())

    def upsert_meta(self, primary_key, metadata_dict):
        # your code here
        upserted_meta = TSDBOp_UpsertMeta(primary_key, metadata_dict)
        return self._send(upserted_meta.to_json())

    def select(self, metadata_dict={}, fields=None, additional=None):
        # your code here
        select_op = TSDBOp_Select(metadata_dict, fields, additional)
        return self._send(select_op.to_json())

    def augmented_select(self, proc, target, arg=None, metadata_dict={}, additional=None):
        #your code here
        aug_select_op = TSDBOp_AugmentedSelect(proc, target, arg, md, additional)
        return self._send(aug_select_op.to_json())

    def add_trigger(self, proc, onwhat, target, arg):
        # your code here
        add_trigger_op = TSDBOp_AddTrigger(proc, onwhat, target, arg)
        return self._send(add_trigger_op.to_json())

    def remove_trigger(self, proc, onwhat):
        # your code here
        remove_trigger_op = TSDBOp_RemoveTrigger(proc, onwhat)
        return self._send(remove_trigger_op.to_json())

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload

    async def _send_coro(self, msg, loop):
        # your code here
        print ("C> sending:", msg)
        serialized_msg = serialize(msg)

        reader, writer = await asyncio.open_connection('127.0.0.1', self.port, loop = loop)

        #print('Send:', msg)
        writer.write(serialized_msg)

        data = await reader.read(8192)
        #print('Received: %r' % data)

        deserializer = Deserializer();
        deserializer.append(data)
        if deserializer.ready():
            response = deserializer.deserialize()
            status = response['status']
            payload = response['payload']

        print ("C> status:", status)
        print ("C> payload", payload)
        return status, payload

    #call `_send` with a well formed message to send.
    #once again replace this function if appropriate
    def _send(self, msg):
        loop = asyncio.get_event_loop()
        coro = asyncio.ensure_future(self._send_coro(msg, loop))
        loop.run_until_complete(coro)
        return coro.result()