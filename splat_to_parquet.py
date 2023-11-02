import numpy as np
import pandas as pd
import argparse

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from parquet_to_splat import splat_columns

def splat_to_data_frame(input_file):
    float_cols, uint8_cols, int_cols = splat_columns()
    
    n_p = len(uint8_cols) // 4
    packed_cols = float_cols + ['packed_%d' % i for i in range(n_p)]
    
    #print(packed_cols)

    flat_array = np.fromfile(input_file, dtype='uint32')
    
    array_reshaped = flat_array.reshape((len(packed_cols), -1), order='F').T
    df = pd.DataFrame(array_reshaped, columns=packed_cols)
    for c in float_cols:
        df[c] = df[c].view(np.float32)
        
    unpacked_cols = {}
    for i, c in enumerate(uint8_cols):
        col_idx = i // 4
        sub_idx = i % 4
        packed_col = df['packed_%d' % col_idx]
        scale = 1
        if c not in int_cols:
             scale = 1 / float(0xff) 
        #else:
        #    print(packed_col)
        unpacked_cols[c] = ((packed_col.to_numpy().astype(int) // (2**(sub_idx*8))) % 256) * scale
    
    for i in range(n_p):
        df.pop('packed_%d' % i)
    
    for c in uint8_cols:
        df[c] = unpacked_cols[c]
        
    # print(df)

    return df
    
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet to Gaussian Splatting flat data converter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='Splat input file')
        parser.add_argument('output_file', type=argparse.FileType('wb'), help='Parquet output file')
        return parser.parse_args()
    
    args = parse_args()
    df = splat_to_data_frame(args.input_file)
    df.to_parquet(args.output_file)

