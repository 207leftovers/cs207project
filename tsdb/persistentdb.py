from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import pickle
import os
import struct
import portalocker
import ast
from TimeSeries import TimeSeries

# This dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}

class DBRow:
    "Stores a row of data for a primary key"        
    def __init__(self, pk, defaults, ts=None):
        self.pk = pk
        self.ts = ts
        self.row = defaults
        
    def update(self, field_name, value):
        if field_name == 'ts':
            self.ts = value
        else:
            self.row[field_name] = value
        
    def get_field(self, field_name):
        if field_name == 'ts':
            return self.ts
        else:
            return self.row[field_name]
    
    def to_string(self):
        a_dict = {'pk': self.pk, 'ts_t': self.ts._times.tolist(), 'ts_v': self.ts._values.tolist(), 'row': self.row}
        return str(a_dict)

    def row_from_string(a_string):
        a_dict = ast.literal_eval(a_string)
        pk = a_dict['pk']
        ts_times = a_dict['ts_t']
        ts_values = a_dict['ts_v']
        row = a_dict['row']
        return DBRow(pk, row, TimeSeries(ts_times, ts_values))


def metafiltered(d, schema, fieldswanted):
    d2 = {}
    if len(fieldswanted) == 0:
        keys = [k for k in d.keys() if k != 'ts']
    else:
        keys = [k for k in d.keys() if k in fieldswanted]
    for k in keys:
        if k in schema:
            d2[k] = schema[k]['convert'](d[k])
    return d2

class ValueRef(object):
    " a reference to a string value on disk"
    def __init__(self, referent=None, address=0):
        self._referent = referent #value to store
        self._address = address #address to store at
        
    @property
    def address(self):
        return self._address
    
    def prepare_to_store(self, storage):
        pass

    @staticmethod
    def referent_to_bytes(referent):
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        return bytes.decode('utf-8')
    
    def get(self, storage):
        "read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "store bytes for value to disk"
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))
            
class BinaryNodeRef(ValueRef):
    "reference to a btree node on disk"
    
    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        "have a node store its refs"
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        "use pickle to convert node to bytes"
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )

class BinaryNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        "clone a node with some changes from another one"
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
        )

    def __init__(self, left_ref, key, value_ref, right_ref):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)
        
class BinaryTree(object):
    "Immutable Binary Tree class. Constructs new tree on changes"
    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()
        self._keys = set()
        
    def commit(self):
        "Changes are final only when committed"
        #triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        #make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "get reference to new tree if it has changed"
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())
        
    def has_key(self, key):
        "Checks if the key is in the tree"
        return key in self._keys
        
    def get(self, key):
        "get value for a key"
        #your code here
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value):
        "Set a new value in the tree. Will cause a new tree"
        # Try to lock the tree. If we succeed make sure
        # we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # Get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # Insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)
        # Add key to the set
        self._keys.add(key)
        
    def _insert(self, node, key, a_value_ref):
        "Insert a new node creating a new path from root"
        #create a tree if there was none so far
        new_node = node
        if node is None:
            # New node
            new_node = BinaryNode(
                BinaryNodeRef(), key, a_value_ref, BinaryNodeRef())
        elif key < node.key:
            "Key less than node.key"
            new_node = BinaryNode(
                self._insert(
                    self._follow(node.left_ref), key, a_value_ref), 
                node.key, node.value_ref, node.right_ref)
        elif key > node.key:
            "Key more than node.key"
            new_node = BinaryNode(
                node.left_ref, node.key, node.value_ref,
                self._insert(
                    self._follow(node.right_ref), key, a_value_ref))
        else: 
            # Update an existing node
            new_node = BinaryNode.from_node(node, value_ref=a_value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        "Delete node with key, creating new tree and path"
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)
        # Remove the key from the dictionary of keys
        self._keys.remove(key)
        
    def _delete(self, node, key):
        "Underlying delete implementation"
        if node is None:
            raise KeyError
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key))
        else:
            left = self._follow(node.left_ref)
            right = self._follow(node.right_ref)
            if left and right:
                replacement = self._find_max(left)
                left_ref = self._delete(
                    self._follow(node.left_ref), replacement.key)
                new_node = BinaryNode(
                    left_ref,
                    replacement.key,
                    replacement.value_ref,
                    node.right_ref,
                )
            elif left:
                return node.left_ref
            else:
                return node.right_ref
        return BinaryNodeRef(referent=new_node)

    def _follow(self, ref):
        "Get a node from a reference"
        #calls BinaryNodeRef.get
        return ref.get(self._storage)
    
    def _find_max(self, node):
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node

class Storage(object):
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        "Guarantee that the next write will start on a sector boundary"
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        "If not locked, lock the file for writing"
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        "Go to beginning of file which is on sec boundary"
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        "Write data to disk, returning the adress at which you wrote it"
        #first lock, get to end, get address to return, write size
        #write data, unlock <==WRONG, dont want to unlock here
        #your code here
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        self.lock()
        self._f.flush()
        #make sure you write root address at position 0
        self._seek_superblock()
        #write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        #read the first integer in the file
        #your code here
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        return self._f.closed
        
class PersistentDB(object):

    def __init__(self, schema, pkfield, f='data', overwrite=False):
        self.schema = schema
        self.pkfield = pkfield
       
        #self.fields = []
        self.defaults = {}
        
        self._storage = {}
        self._trees = {}
        
        meta_info_filename = 'db_meta'
        
        path_to_db_files = 'db_files/' + f + '/'
        if not os.path.exists(path_to_db_files):
            os.makedirs(path_to_db_files)
        
        # The highest transaction sequence number
        self.tid_seq = 0
        
        # Transaction Table
        # "contains all transactions that are currently running and the Sequence Number of the last log entry they caused"
        self.tt = {}
        
        # Load meta information if the path exists and we are not overwriting
        if os.path.exists(path_to_db_files+meta_info_filename) and not overwrite:
            with open(path_to_db_files+meta_info_filename, 'rb', buffering=0) as fd:
                self.pkfield, self.schema = pickle.load(fd)
                # Ensure the schema matches 
                if (schema is not None) and (schema != self.schema):
                    raise ValueError("Schemas don't match")
                if self.pkfield != pk_field:
                    raise ValueError("PKs don't match")
        else:
            pass
            # TODO: !!!
            # Write the meta information to file
            #with open(path_to_db_files+meta_info_filename,'wb',buffering=0) as fd:
            #    pickle.dump((self.pkfield, dict(self.schema)), fd)

        for s in schema:            
            indexinfo = schema[s]['index']
            convert = schema[s]['convert']
            default = schema[s]['default']
            
            if indexinfo is not None:
                #self.fields.append(s)
                self.defaults[s] = default
            
            # Use binary search trees for highcard/numeric
            # TODO:
            # Use bitmaps for lowcard/str_or_factor
            # Always index PK no matter what indexinfo says
            
            # TODO:!
            #if indexinfo is not None or s == 'pk':
            if s == 'pk':
                f = self.open_file(path_to_db_files + s, overwrite)
                self._storage[s] = Storage(f)
                # if convert in ():
                self._trees[s] = BinaryTree(self._storage[s])
                # else:
                #    self._trees[s] = BitMask(self._storage[s])
                
    def open_file(self, filename, overwrite):
        try:
            if overwrite:
                f = open(filename, 'wb+')
            else:
                f = open(filename, 'r+b')
        except IOError:
            fd = os.open(filename, os.O_RDWR | os.O_CREAT)
            f = os.fdopen(fd, 'r+b')
        return f
    
    def next_tid_val(self):
        self.tid_seq += 1
        return self.tid_seq
    
    # Check to ensure that this tid refers to an open transaction
    def check_tid_open(self, tid):
        if tid not in self.tt:
            raise ValueError('No valid open transaction %d!' % tid)
                
    # Begin the transaction
    def begin_transaction(self):
        # Generate a new tid
        tid = self.next_tid_val()
        
        # Add this tid to the transaction table
        self.tt[tid] = set()
        
        return tid
        
    # Commit the transaction
    def commit(self, tid):
        self.check_tid_open(tid)

        open_trees = self.tt[tid]
        for tree in open_trees:
            self._assert_not_closed(tree)
            self._trees[tree].commit()
        
        # remove this tid from the transaction table
        del self.tt[tid]
        
    # Rollback the transaction
    def rollback(self, tid):
        self.check_tid_open(tid)
        
        open_trees = self.tt[tid]
        for tree in open_trees:
            # TODO:
            pass
        
        del self.tt[tid]

    def _assert_not_closed(self, field):
        if self._storage[field].closed:
            raise ValueError('Database closed:', field)

    def close(self):
        self._storage.close()

    def get(self, key):
        #self._assert_not_closed()
        return self._tree.get(key)

    # Insert a timeseries for a specific primary key
    def insert_ts(self, tid, pk, ts):
        self.check_tid_open(tid)
        self._assert_not_closed('pk')
        self.tt[tid].add('pk')
        
        if self._trees['pk'].has_key(pk):
            raise ValueError('Duplicate primary key found during insert')
        else:
            row = DBRow(pk, self.defaults, ts)
            self._trees['pk'].set(pk, row.to_string())

    # Delete a timeseries for a specific primary key
    def delete_ts(self, tid, pk):
        self.check_tid_open(tid)
        self._assert_not_closed('pk')
        self.tt[tid].add('pk')
        
        if self._trees['pk'].has_key(pk):
            # Remove the timeseries from the db
            self._trees['pk'].delete(pk)
        else:
            raise ValueError('Primary key %d not found during deletion' % pk)
    
    # Upsert data for a specific primary key based on a dictionary of 
    # fields and values to upsert
    def upsert_meta(self, tid, pk, meta):
        "Implement upserting field values, as long as the fields are in the schema."
        self.check_tid_open(tid)
        
        if self._trees['pk'].has_key(pk):
            # Get the row if it already exists
            row_str = self._trees['pk'].get(pk)
            row = DBRow.row_from_string(row_str)
        else:
            # Create the row if it doesn't exist
            row = DBRow(pk, self.defaults)
            
        # Look through the fields and upsert their values
        for key in meta:         
            if key in self.schema:
                self.tt[tid].add(key)
                row.update(key, meta[key])
                
        self._trees['pk'].set(pk, row.to_string())

        # Update the indices
        # TODO: !!!
        #self.update_indices(pk)
    
    
class old_DictDB:
    "Database implementation in a dict"
    def __init__(self, schema, pkfield):
        self.indexes = {}
        
    def index_bulk(self, pks=[]):
        if len(pks) == 0:
            pks = self.rows
        for pkid in self.pks:
            self.update_indices(pkid)

    def update_indices(self, pk):
        row = self.rows[pk]
        for field in row:
            v = row[field]
            if field in self.indexes:
                idx = self.indexes[field]
                idx[v].add(pk)
                
    def delete_indices(self, pk):
        row = self.rows[pk]
        for field in row:
            v = row[field]
            if field in self.indexes:
                idx = self.indexes[field]
                
                # Remove this pk from this index value's dict
                idx[v].remove(pk)
                
                # If this value has no more rows, then remove it
                if len(idx[v]) == 0:
                    del idx[v]

    def select(self, tid, meta, fields, additional):
        self.check_tid_open(tid)
        
        # If fields is None: return only pks like so: 
        #     [pk1,pk2],[{},{}]
        
        # If fields is [], this means all fields except for the 'ts' field looks like:
        #     ['pk1',...],[{'f1':v1, 'f2':v2},...]
        
        # If the names of fields are given in the list, include only those fields. 
        # `ts` ia an acceptable field and can be used to just return time series.
        # see tsdb_server to see how this return value is used
        
        # 'additional' is a dictionary. It has two possible keys:
        #     (a){'sort_by':'-order'}, or {'sort_by':'+order'} 
        # where order must be in the schema AND have an index. 
        #     (b) limit: 'limit':10
        # which will give you the top 10 in the current sort order.
        result_set = []

        # META
        # Select the keys that matches the metadata
        for pk in self.rows.keys():
            satisfied = True
            for meta_key in meta.keys():
                if meta_key not in self.rows[pk].keys():
                    satisfied = False
                else:
                    # range operators are stored in a dict
                    if isinstance(meta[meta_key], dict):
                        for operator, value in meta[meta_key].items():  
                            if (not OPMAP[operator](self.rows[pk][meta_key], value)):
                                satisfied = False

                    else:
                        if self.rows[pk][meta_key] is not meta[meta_key]:
                            satisfied = False
            if satisfied is True:
                result_set.append(pk)

        matchedfielddicts = []
        
        # FIELDS
        # select the correct fields
        for pk in result_set:
            matched_field = {}
            # If fields is None, just return the primary keys
            if fields == None:
                # Do nothing
                pass
            elif len(fields) is 0:
                for row_field in self.rows[pk]:

                    #skip the ts 
                    if row_field is 'ts':
                        continue
                    matched_field[row_field] = self.rows[pk][row_field]                    
            else:
                for field in fields:
                    if field in self.rows[pk]:
                        matched_field[field] = self.rows[pk][field]

            matchedfielddicts.append(matched_field)

        # ADDITIONAL
        if additional is None:
            return result_set, matchedfielddicts
        else:
            # We have to do sorting and limiting
            result_sorted = []
            
            # SORTING
            # Get the sorted by keyword
            if 'sort_by' in additional.keys():
                sorted_by = additional['sort_by']
                order_list = []

                # Get direction of sorting
                is_decreasing = True
                if sorted_by[0] == '+':
                    is_decreasing = False

                # Get the keyword
                sorted_by = sorted_by[1:]

                # Get the order for the result_set
                for pk in result_set:
                    order_list.append(self.rows[pk][sorted_by])

                result_tuple = []

                # Then we combine everything into a tuple
                for x in range(len(result_set)):
                    result_tuple.append((result_set[x], matchedfielddicts[x], order_list[x]))

                result_sorted = sorted(result_tuple, key=lambda x: x[2], reverse=is_decreasing)

            else:
                # We are going to skip sorting and move on to limiting
                for x in range(len(result_set)):
                    result_sorted.append((result_set[x], matchedfielddicts[x]))

            # LIMITING
            if 'limit' in additional.keys():
                limit_num = additional['limit']
                result_sorted = result_sorted[:limit_num]

            result_set_sorted = []
            matchedfielddicts_sorted = []

            for x in range(len(result_sorted)):
                result_set_sorted.append(result_sorted[x][0])
                matchedfielddicts_sorted.append(result_sorted[x][1])

            return result_set_sorted, matchedfielddicts_sorted