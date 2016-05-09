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
            
    async def begin_transaction(self):
        tx = TSDBOp_BeginTransaction()
        
        value =  await self._send(tx.to_json())
        print('tsdb_client', value)
        return value
        
    async def insert_ts(self, tid, primary_key, ts):
        '''
        Inserts a TimeSeries into the database.
        Parameters
        ----------
        primary_key : String, Int, etc.
            The primary key for the TimeSeries entry
        ts : TimeSeries
            TimeSeries to be inserted into the database
        Returns
        -------
        The result of the operation
        '''
        InsertedTS = TSDBOp_InsertTS(tid, primary_key, ts)
        return await self._send(InsertedTS.to_json())

    # Deletes a TimeSeries from the DB based on its PK
    async def delete_ts(self, tid, primary_key):
        delete_ts_op = TSDBOp_DeleteTS(tid, primary_key)
        return await self._send(delete_ts_op.to_json())

    # Upserts information into the DB based on the PK, and a 
    # dictionary of fields and values stored in metadata_dict
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

    async def _send_coro(self, msg, loop):
        # your code here
        print ("C> sending:", msg)
        serialized_msg = serialize(msg)

        reader, writer = await asyncio.open_connection('127.0.0.1', self.port, loop = loop)

        writer.write(serialized_msg)
        await writer.drain()

        # 8192
        data = await reader.read()
        #print('Received: %r' % data)
        writer.close()

        deserializer = Deserializer();
        deserializer.append(data)
        if deserializer.ready():
            response = deserializer.deserialize()
            print('C> response', response)
            status = TSDBStatus(response['status'])
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