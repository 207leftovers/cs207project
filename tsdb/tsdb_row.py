import ast
import timeseries as ts

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
        return DBRow(pk, row, ts.TimeSeries(ts_times, ts_values))