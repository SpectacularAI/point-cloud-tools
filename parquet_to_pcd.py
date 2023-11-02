import numpy as np
import pandas as pd
import sys
import argparse
import struct
from io import StringIO

def dataframe_to_pcd(df, out_file, include_rgb=False):
    cols = ['x', 'y', 'z']
    if include_rgb:
        cols.append('rgb')
        r,g,b = [df[c].astype(np.uint32) for c in 'rgb']
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
 
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet point cloud converter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='Parquet input file')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='PCD output file')
        parser.add_argument('--rgb', action='store_true')
        return parser.parse_args()
    
    args = parse_args()

    df = pd.read_parquet(args.input_file)
    dataframe_to_pcd(df, args.output_file, include_rgb=args.rgb)

