import pandas as pd
import numpy as np
import struct
import re
from io import StringIO

# mostly ChatGPT-generated
def dataframe_to_pcd_stream(df, out_file, include_rgb=True):
    cols = ['x', 'y', 'z']
    colors = ['red', 'green', 'blue']
    if include_rgb and all([c in df.columns or c[0] in df.columns for c in colors]):
        cols.append('rgb')
        r,g,b = [df[c].astype(np.uint32) if c in df.columns else df[c[0]].astype(np.uint32) for c in colors]
        packed_rgb = (r * (2**16)) + (g * (2**8)) + b
        df['rgb'] = packed_rgb.apply(lambda x: struct.unpack('f', struct.pack('I', x))[0])
        
    # print(df)
    
    header = ''.join([
        "VERSION .7\n",
        "FIELDS {columns}\n",
        "SIZE {col_sizes}\n",
        "TYPE {col_types}\n",
        "COUNT {col_count}\n",
        "WIDTH {size}\n",
        "HEIGHT 1\n",
        "VIEWPOINT 0 0 0 1 0 0 0\n",
        "POINTS {size}\n",
        "DATA ascii\n"
    ]).format(
        columns=' '.join(cols),
        size=len(df),
        col_sizes=' '.join(['4']*len(cols)),
        col_types=' '.join(['F']*len(cols)),
        col_count=' '.join(['1']*len(cols)))
    
    # Convert the DataFrame to a list of strings
    b = StringIO()
    df[cols].to_csv(b, sep=' ', index=False, header=False)
    
    out_file.write(header + '\n')
    out_file.write(b.getvalue().strip())
    
def dataframe_to_pcd(df, out_file, **kwargs):
    with open(out_file, 'wt') as f:
        dataframe_to_pcd_stream(df, f, **kwargs)
