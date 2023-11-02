import numpy as np
import pandas as pd
import argparse

def splat_columns():
    pos_cols = 'x,y,z'.split(',')
    scale_cols = 'cov_s0,cov_s1,cov_s2'.split(',')
    rot_cols = 'cov_q0,cov_q1,cov_q2,cov_q3'.split(',')
    alpha_cols = ['alpha0']
    # ignore the rest of the spherical harmonic coefficients like r_sh1, r_sh2, etc.
    color_cols = 'r,g,b'.split(',')
    
    int_cols = set(color_cols + alpha_cols)
    
    float_cols = pos_cols + scale_cols
    uint8_cols = color_cols + alpha_cols + rot_cols
    
    return float_cols, uint8_cols, int_cols

def convert_splat_colors(df):
    def sh_zero_order(col):
        # see https://github.com/wanmeihuali/taichi_3d_gaussian_splatting/blob/main/taichi_3d_gaussian_splatting/SphericalHarmonics.py
        magic_coeff = 0.28209479177387814
        normalized = magic_coeff * col
        col = 1 / (1 + np.exp(-normalized))
        return col

    for c in 'rgb':
        df[c] = sh_zero_order(df['%s_sh0' % c])
    
    return df

def dataframe_to_flat_array(df):
    convert_splat_colors(df)
    
    #print(df.columns)
    #import matplotlib.pyplot as plt
    #for c in 'rgb':
    #    cc = df[c]
    #    cc = cc[np.isfinite(cc)]
    #    plt.hist(cc, bins=100); plt.title(c); plt.show()
    
    float_cols, uint8_cols, int_cols = splat_columns()
    dtypes = [(f, 'float32') for f in float_cols] + [(u, 'uint8') for u in uint8_cols]

    # Create a structured array with the same number of rows as the DataFrame
    structured_array = np.zeros(df.shape[0], dtype=dtypes)

    # Assign the DataFrame columns to the structured array
    for column, dtype in dtypes:
        v = df[column].values
        if dtype == 'uint8':
            if column in int_cols:
                v = np.clip(v * 0xff, 0, 0xff).astype(np.uint8)
            else:
                v = (((v + 1.0)*0.5) * 0xff).astype(np.uint8)
        structured_array[column] = v
    
    flat_array = structured_array.view('uint8')
    return flat_array

if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet to Gaussian Splatting flat data converter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='Parquet input file')
        parser.add_argument('output_file', type=argparse.FileType('wb'), help='Splat output file')
        return parser.parse_args()
    
    args = parse_args()

    df = pd.read_parquet(args.input_file)
    flat_array = dataframe_to_flat_array(df)
    flat_array.tofile(args.output_file)

