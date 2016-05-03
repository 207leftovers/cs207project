from collections import defaultdict
from operator import and_
from functools import reduce
import operator

# this dictionary will help you in writing a generic select operation
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
        #print('UPSERTING!!!')
        "implement upserting field values, as long as the fields are in the schema."
        # Insert the primary key if it wasn't present
        if pk not in self.rows:
            self.rows[pk] = {'pk': pk}
            
        for key in meta:         
            if key in self.schema:
                #raise TypeError('UPSERTING KEY: '+str(key)) 
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

    def select(self, meta, fields, additional):
        # your code here
        # if fields is None: return only pks
        # like so [pk1,pk2],[{},{}]
        # if fields is [], this means all fields
        # except for the 'ts' field. Looks like
        # ['pk1',...],[{'f1':v1, 'f2':v2},...]
        # if the names of fields are given in the list, include only those fields. `ts` ia an
        # acceptable field and can be used to just return time series.
        # see tsdb_server to see how this return
        # value is used
        # additional is a dictionary. It has two possible keys:
        # (a){'sort_by':'-order'} or {'sort_by':'+order'} where order
        # must be in the schema AND have an index. (b) limit: 'limit':10
        # which will give you the top 10 in the current sort order.

        result_set = []

        print (self.rows)

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