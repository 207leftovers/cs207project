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

class PersistentDB(object):

    def write_meta_to_disk(self):
        with open(self.path_to_db_files+self.meta_info_filename, 'wb') as fd:
                pickle.dump({
                    'pkfield': self.pkfield,
                    'schema': self.schema,
                    'vps': self.vps
                }, fd)
                
    def read_meta_from_dist(self):
        with open(self.path_to_db_files+self.meta_info_filename, 'rb', buffering=0) as fd:
            try:
                d = pickle.load(fd)
                self.pkfield = d['pkfield']
                self.schema = d['schema']
                self.vps = d['vps']
            except EOFError: 
                raise EOFError
                
    def open_storage(self, s, convert, overwrite):
        # Always index PK no matter what indexinfo says
        if s == 'pk':
            f = self.open_file(self.path_to_db_files + s, overwrite)
            self._storage[s] = Storage(f)
            self._trees[s] = BinaryTree(self._storage[s])
        else:
            # Use binary search trees for highcard/numeric
            # TODO: Use bitmaps for lowcard/str_or_factor
            f = self.open_file(self.path_to_db_files + s, overwrite)
            self._storage[s] = Storage(f)
            self._trees[s] = ArrayBinaryTree(self._storage[s], convert)

    
    def __init__(self, schema, pkfield, f='data', overwrite=False):
        # Augment the schema by adding an indicator column for vantage points
        schema['vp'] = {'convert': bool, 'index': 1, 'default': False}
        
        # METAINFO
        self.meta_info_filename = 'db_meta'
        
        self.pkfield = pkfield
        self.schema = schema
        self.vps = []

        # LOAD INDICES FROM FILES
        self._storage = {}
        self._trees = {}
        
        self.path_to_db_files = 'db_files/' + f + '/'
        if not os.path.exists(self.path_to_db_files):
            os.makedirs(self.path_to_db_files)
        
        # The highest transaction sequence number
        self.tid_seq = 0        
        # Transaction Table
        # Contains all transactions that are currently running and the Sequence Number of the last log entry they caused
        self.tt = {}

        # Load meta information if the path exists and we are not overwriting
        if os.path.exists(self.path_to_db_files+self.meta_info_filename) and not overwrite:
            # Read in the metadata from disk
            self.read_meta_from_dist()
            # Ensure the schema matches (uness the passed in schema was None)
            if (schema is not None) and len(schema) != len(self.schema):
                raise ValueError("Schemas don't match")
            if self.pkfield != pkfield:
                raise ValueError("PKs don't match")
        else:
            self.schema = schema
            # Write the meta information to file
            self.write_meta_to_disk()
        
        # Opens the storage
        self.defaults = {}
        self.validfields = ['ts']
        
        for s in self.schema:            
            indexinfo = self.schema[s]['index']
            convert = self.schema[s]['convert']
            default = self.schema[s]['default']
        
            if indexinfo is not None or s=='pk':
                self.validfields.append(s)
                if s != 'pk':
                    self.defaults[s] = default                
                # OPEN THE STORAGE! RELEASE THE KRAKEN!
                self.open_storage(s, convert, overwrite)
                
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
        
        # Update the meta data that is stored on disk
        self.write_meta_to_disk()

        open_fields = self.tt[tid]
        for field in open_fields:
            self._assert_not_closed(field)
            self._trees[field].commit()
            self._storage[field].unlock()
        # remove this tid from the transaction table
        del self.tt[tid]
        
    # Rollback the transaction
    def rollback(self, tid):
        self.check_tid_open(tid)
        
        # Read the meta data that is stored on disk
        self.read_meta_from_dist()
        
        open_fields = self.tt[tid]
        if 'pk' not in open_fields:
            open_fields |= {'pk'}
        for field in open_fields:
            print('DB> Rolling back ', field)
            #self._assert_not_closed(field)
            self._trees[field].rollback()
            #self._storage[field].close()
            #self.open_storage(field, self.schema[field]['convert'], False)
        
        del self.tt[tid]

    def _assert_not_closed(self, field):
        if self._storage[field].closed:
            raise ValueError('Database closed:', field)

    def close(self):
        for key in self._storage.keys():
            self._storage[key].close()

    def get_row(self, pk):
        self._assert_not_closed('pk')
        return self._trees['pk'].get_as_row(pk)
    
    def create_vp(self, tid, pk):
        self.check_tid_open(tid)
        ts = self.get_row(pk).ts
        #make sure pk are strings
        pk = str(pk)
        self.upsert_meta(tid, pk, {'vp': True})
        
        d_vp = len(self.vps)
        
        fieldname = "d_vp-{}".format(d_vp)
        
        # Augment the schema by adding a column for this vp
        self.schema[fieldname] = {'convert': float, 'index': 1, 'default': 0.0}
        
        # Add to valid fields
        self.validfields.append(fieldname)
        self.vps.append(pk)
        
        f = self.open_file(self.path_to_db_files + fieldname, True)
        self._storage[fieldname] = Storage(f)
        self._trees[fieldname] = ArrayBinaryTree(self._storage[fieldname], float)
        
        return fieldname, ts

    # Insert a timeseries for a specific primary key
    def insert_ts(self, tid, pk, ts):
        self.check_tid_open(tid)
        #make sure pk are strings
        pk = str(pk)
        self._assert_not_closed('pk')
        self.tt[tid].add('pk')
        
        if self._trees['pk'].has_key(pk):
            raise ValueError('Duplicate primary key found during insert')
        else:
            row = DBRow(pk, self.defaults, ts)
            self._trees['pk'].set(pk, row.to_string())
            self.update_indices(pk, row)

    # Delete a timeseries for a specific primary key
    def delete_ts(self, tid, pk):
        self.check_tid_open(tid)
        #make sure pk are strings
        pk = str(pk)
        self._assert_not_closed('pk')
        self.tt[tid].add('pk')
        
        if self._trees['pk'].has_key(pk):
            row = self._trees['pk'].get_as_row(pk)
            # Remove the timeseries from the db
            self._trees['pk'].delete(pk)
            
            self.delete_indices(pk, row)
        else:
            raise ValueError('Primary key not found during deletion')
    
    # Upsert data for a specific primary key based on a dictionary of 
    # fields and values to upsert
    def upsert_meta(self, tid, pk, meta):
        print('UPSERTING', pk, meta)
        "Implement upserting field values, as long as the fields are in the schema."
        self.check_tid_open(tid)
        self._assert_not_closed('pk')
        #make sure pk are strings
        pk = str(pk)
         # Check for 'ts'
        if 'ts' in meta.keys():
            raise ValueError("TimeSeries are not allowed to be upserted")
        
        if self._trees['pk'].has_key(pk):
            # Get the row if it already exists
            row_str = self._trees['pk'].get(pk)
            row = DBRow.row_from_string(row_str)
            # Delete the old indices
            self.delete_indices(pk, row)
        else:
            # Can't upsert metadata on a non-existant row
            raise ValueError("TimeSeries with pk: ", pk, " not present in db")
       
        # Look through the fields and upsert their values
        for key in meta:         
            if key in self.validfields:
                self.tt[tid].add(key)
                row.update(key, meta[key])
                
        self._trees['pk'].set(pk, row.to_string())
        # Update with the new indices
        self.update_indices(pk, row)
        
    def update_indices(self, pk, row):
        "Update the non-pk indices"
        rr = row.row
        for field in rr.keys():
            print('FIED', field)
            if field != 'pk':
                v = rr[field]
                if v is not None:
                    self._trees[field].set(v, pk)
            
    def delete_indices(self, pk, row):
        rr = row.row
        for field in rr.keys():
            v = rr[field]
            if v is not None:
                self._trees[field].delete(v, pk)
                
    def select(self, tid, meta, fields, additional):
        self.check_tid_open(tid)
        self._assert_not_closed('pk')
        
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

        # META
        pks = set(self._trees['pk'].get_all_keys())
        # Select the keys that matches the metadata
        for meta_key in meta.keys():
            # Handle case if it is not a dict
            if isinstance(meta[meta_key], dict):
                opdict=meta[meta_key]
            else:
                opdict={'==':meta[meta_key]}
            
            if meta_key == 'pk':
                # PKs
                # range operators are stored in a dict
                for operator, value in opdict.items():
                    #make sure pk are strings
                    value = str(value)
                    some_pks = set()
                    for pk in pks:
                        if OPMAP[operator](pk, value):
                            some_pks |= set([pk])
                    pks = some_pks
            elif meta_key in self.validfields:
                # Non PK lookups
                all_field_keys = self._trees[meta_key].get_all_keys()
                # range operators are stored in a dict
                for operator, value in opdict.items():  
                    some_field_keys = set()
                    for field_key in all_field_keys:
                        if OPMAP[operator](field_key, value):
                            some_field_keys |= set([field_key])
                    all_field_keys = some_field_keys
                some_pks = set()    
                # Now gather all PKs for these field keys
                for field_key in all_field_keys:
                    some_pks |= set(self._trees[meta_key].get(field_key))
                    
                # Now update the over-all set of pks by finding the intersection
                pks = pks.intersection(some_pks)
        
        matchedfielddicts = []
        
        # FIELDS
        # select the correct fields
        for pk in pks:
            pk_row = self._trees['pk'].get_as_row(pk)

            matched_field = {}
            # If fields is None, just return the primary keys
            if fields == None:
                # Do nothing
                pass
            elif len(fields) is 0:
                # Get all fields but the TimeSeries
                for row_field in self.validfields:
                    # Skip the ts 
                    if row_field == 'ts':
                        continue
                    elif row_field == 'pk':
                        matched_field[row_field] = pk_row.pk
                    else:
                        matched_field[row_field] = pk_row.row[row_field]
            else:
                # Only get the indicated fields
                for field in fields:
                    if field in self.validfields:
                        if field == 'pk':
                            matched_field[field] = pk_row.pk
                        elif field == 'ts':
                            matched_field[field] = pk_row.ts
                        else:
                            matched_field[field] = pk_row.row[field]

            matchedfielddicts.append(matched_field)

        # ADDITIONAL
        if additional is None:
            return list(pks), matchedfielddicts
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
                for pk in pks:
                    pk_row = self._trees['pk'].get_as_row(pk)
                    if sorted_by == 'pk':
                        order_list.append(pk_row.pk)
                    elif sorted_by in self.validfields:
                        order_list.append(pk_row.row[sorted_by])
                    else:
                        order_list.append(0)
                result_tuple = []

                # Then we combine everything into a tuple
                for i, x in enumerate(pks):
                    result_tuple.append((x, matchedfielddicts[i], order_list[i]))

                result_sorted = sorted(result_tuple, key=lambda x: x[2], reverse=is_decreasing)

            else:
                # We are going to skip sorting and move on to limiting
                for i, x in enumerate(pks):
                    result_sorted.append((x, matchedfielddicts[i]))

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