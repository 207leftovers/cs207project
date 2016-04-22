from collections import defaultdict
from operator import and_
from functools import reduce
import operator

# this dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}


class DictDB:
    "Database implementation in a dict"
    def __init__(self, schema, pkfield):
        self.indexes = {}
        self.rows = {}
        self.schema = schema
        self.pkfield = pkfield
        for s in schema:
            indexinfo = schema[s]['index']
            # convert = schema[s]['convert']
            # later use binary search trees for highcard/numeric
            # bitmaps for lowcard/str_or_factor
            if indexinfo is not None:
                self.indexes[s] = defaultdict(set)

    def insert_ts(self, pk, ts):
        if pk not in self.rows:
            self.rows[pk] = {'pk': pk}
        else:
            raise ValueError('Duplicate primary key found during insert')
        self.rows[pk]['ts'] = ts
        self.update_indices(pk)

    def upsert_meta(self, pk, meta):
        "implement upserting field values, as long as the fields are in the schema."
        # your code here

        if pk not in self.rows:
            raise ValueError('primary key not found during upsert')
        else:
            for key in meta:         
                self.rows[pk][key] = meta[key]

        self.update_indices(pk)

    def index_bulk(self, pks=[]):
        if len(pks) == 0:
            pks = self.rows
        for pkid in self.pks:
            self.update_indices(pkid)

    def update_indices(self, pk):
        row = self.rows[pk]
        for field in row:
            v = row[field]
            if self.schema[field]['index'] is not None:
                idx = self.indexes[field]
                idx[v].add(pk)

    def select(self, meta, fields):
        # your code here
        # if fields is None: return only pks
        # like so [pk1,pk2],[{},{}]
        # if fields is [], this means all fields
        #except for the 'ts' field. Looks like
        #['pk1',...],[{'f1':v1, 'f2':v2},...]
        # if the names of fields are given in the list, include only those fields. `ts` ia an
        #acceptable field and can be used to just return time series.
        #see tsdb_server to see how this return
        #value is used

        result_set = []

        #select the keys that matches the metadata
        for pk in self.rows.keys():
            satisfied = True
            for meta_key in meta:
                if meta_key not in self.rows[pk].keys():
                    satisfied = False
                else:
                    #range operators are stored in a dict
                    if isinstance(meta[meta_key], dict):
                        for operator in meta[meta_key]:  
                            if (not OPMAP[operator] (self.rows[pk][meta_key], meta[meta_key][operator] )):
                                satisfied = False

                        
                    else:
                        if self.rows[pk][meta_key] is not meta[meta_key]:
                            satisfied = False
            if satisfied is True:
                result_set.append(pk)

        matchedfielddicts = []

        if fields is None:
            return result_set, None


        #select the correct fields
        for pk in result_set:
            matched_field = {}
            if len(fields) is 0:
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

        return result_set, matchedfielddicts


