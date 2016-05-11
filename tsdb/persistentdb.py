from collections import defaultdict
from operator import and_
from functools import reduce
import operator
import pickle
import os
import struct
import portalocker
from tsdb.tsdb_row import *
from tsdb.tsdb_indexes import *

# This dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}

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
        
class PersistentDB(object):

    def __init__(self, schema, pkfield, f='data', overwrite=False):
        self.schema = schema
        self.pkfield = pkfield
       
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
            
            if indexinfo is not None or s=='pk':
                self.defaults[s] = default
            
                # Use binary search trees for highcard/numeric
                # TODO:
                # Use bitmaps for lowcard/str_or_factor
                # Always index PK no matter what indexinfo says
            
                if s == 'pk':
                    f = self.open_file(path_to_db_files + s, overwrite)
                    self._storage[s] = Storage(f)
                    self._trees[s] = BinaryTree(self._storage[s])
                else:
                    # if convert in ():
                    # else:
                    #    self._trees[s] = BitMask(self._storage[s])
                    f = self.open_file(path_to_db_files + s, overwrite)
                    self._storage[s] = Storage(f)
                    self._trees[s] = ArrayBinaryTree(self._storage[s])
                
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

        open_fields = self.tt[tid]
        for field in open_fields:
            self._assert_not_closed(field)
            self._trees[field].commit()
        
        # remove this tid from the transaction table
        del self.tt[tid]
        
    # Rollback the transaction
    def rollback(self, tid):
        self.check_tid_open(tid)
        
        open_fields = self.tt[tid]
        for field in open_fields:
            self._assert_not_closed(field)
            self._storage[field].unlock()
        
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
            self.update_indices(pk, row, True)

    # Delete a timeseries for a specific primary key
    def delete_ts(self, tid, pk):
        self.check_tid_open(tid)
        self._assert_not_closed('pk')
        self.tt[tid].add('pk')
        
        if self._trees['pk'].has_key(pk):
            row = self._trees['pk'].get_as_row(pk)
            # Remove the timeseries from the db
            self._trees['pk'].delete(pk)
            
            self.delete_indices(pk, row)
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
        self.update_indices(pk, row, False)
        
    def update_indices(self, pk, row, new):
        "Update the non-pk indices"
        for field in row.row.keys():
            v = row[field]
            if field in self.indexes:
                idx = self.indexes[field]
                idx[v].add(pk)
        
    
class old_DictDB:
    "Database implementation in a dict"
    def __init__(self, schema, pkfield):
        self.indexes = {}
        
    def index_bulk(self, pks=[]):
        if len(pks) == 0:
            pks = self.rows
        for pkid in self.pks:
            self.update_indices(pkid)

    
                
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