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
        times = ts.times()
        values = ts.values()
        times =  map(str, times)
        values =  map(str, values)
        ts_dict = dict(zip(times, values))
        InsertedTS = TSDBOp_InsertTS(primary_key, ts_dict)
        serialized_ts = serialize(InsertedTS.to_json())
        return self._send(serialized_ts)

    def upsert_meta(self, primary_key, metadata_dict):
        # your code here
        upserted_meta = TSDBOp_UpsertMeta(primary_key, metadata_dict)
        serialized_ts = serialize(upserted_meta.to_json())
        return self._send(serialized_ts)


    def select(self, metadata_dict={}):
        # your code here
        select_op = TSDBOp_Select(metadata_dict)
        serialized_ts = serialize(select_op.to_json())
        return self._send(serialized_ts)

    # Feel free to change this to be completely synchronous
    # from here onwards. Return the status and the payload

    async def _send_coro(self, msg, loop):
        # your code here

        reader, writer = await asyncio.open_connection('127.0.0.1', self.port, loop = loop)

        #print('Send:', msg)
        writer.write(msg)

        data = await reader.read(8192)
        #print('Received: %r' % data)

        deserializer = Deserializer();
        deserializer.append(data)
        if deserializer.ready():
            response = deserializer.deserialize()
            status = response['status']
            payload = response['payload']

        return status, payload

    #call `_send` with a well formed message to send.
    #once again replace this function if appropriate
    def _send(self, msg):
        loop = asyncio.get_event_loop()
        coro = asyncio.ensure_future(self._send_coro(msg, loop))
        loop.run_until_complete(coro)
        return coro.result()
