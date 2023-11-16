import numpy as np
import pandas as pd

def splat_columns():
    pos_cols = 'x,y,z'.split(',')
    scale_cols = 'cov_s0,cov_s1,cov_s2'.split(',')
    rot_cols = 'cov_q3,cov_q0,cov_q1,cov_q2'.split(',') # note: xyzw -> wxyz
    alpha_cols = ['a']
    # ignore the rest of the spherical harmonic coefficients like r_sh1, r_sh2, etc.
    color_cols = 'r,g,b'.split(',')
    
    float_cols = pos_cols + scale_cols
    uint8_cols = color_cols + alpha_cols + rot_cols
    
    uint8_ranges = {
        q: [-1.0, 1.0] for q in rot_cols
    }
    uint8_ranges['a'] = [0.0, 1.0]
    for c in color_cols: uint8_ranges[c] = [0, 255]
    return float_cols, uint8_cols, uint8_ranges

def convert_data_to_splat(df):
    # already converted
    if 'r_sh0' not in df.columns: return df
    
    def sh_zero_order(col):
        # see https://github.com/wanmeihuali/taichi_3d_gaussian_splatting/blob/main/taichi_3d_gaussian_splatting/SphericalHarmonics.py
        magic_coeff = 0.28209479177387814
        normalized = magic_coeff * col
        col = 1 / (1 + np.exp(-normalized))
        return col

    for c in 'rgb':
        if c not in df.columns:
            df[c] = sh_zero_order(df['%s_sh0' % c]) * 255
    
    DEBUG_SCALING = 1
    for cov_i in range(3):
        c = 'cov_s%d' % cov_i
        df[c] = np.exp(df[c]) * DEBUG_SCALING

    NORMALIZE = True
    if NORMALIZE:
        inv_len = 1.0 / np.sqrt(np.sum(df[['cov_q%d' % i for i in range(4)]].values**2, axis=1))
        for i in range(4):
            df['cov_q%d' % i] *= inv_len
            
    df['a'] = 1 / (1 + np.exp(-df['alpha0']))
    
    return df
    
def rename_inria_columns(df):
    r = {
        'opacity': 'alpha0',
        'rot_0': 'cov_q0',
        'rot_1': 'cov_q1',
        'rot_2': 'cov_q2',
        'rot_3': 'cov_q3'
    }
    for i in range(3):
        r['scale_%d' % i] = 'cov_s%d' % i
        r['f_dc_%d' % i] = '%s_sh0' % ('rgb'[i])

    for i in range(45):
        r['f_rest_%d' % i] = '%s_sh%d' % ('rgb'[i // 15], ((i%15) + 1))

    return df.rename(columns=r, inplace=False)

def rename_nerfstudio_columns(df):    
    # q0,q1,q2=xyz, q3=w
    r = {
        'opacity': 'alpha0',
        'rot_0': 'cov_q3',
        'rot_1': 'cov_q0',
        'rot_2': 'cov_q1',
        'rot_3': 'cov_q2',
        'red': 'r',
        'green': 'g',
        'blue': 'b'
    }
    for i in range(3):
        r['scale_%d' % i] = 'cov_s%d' % i
        r['f_dc_%d' % i] = '%s_sh0' % ('rgb'[i])
        
        
    return df.rename(columns=r, inplace=False)
    
def analyze_columns(df):
    print(df.columns)
    import matplotlib.pyplot as plt
    for c in 'alpha0,cov_q0,cov_q1,cov_q2,cov_q3,a,r,g,b,cov_s0,cov_s1,cov_s2'.split(','):
        cc = df[c]
        cc = cc[np.isfinite(cc)]
        plt.hist(cc, bins=256); plt.title(c); plt.show()

def dataframe_to_flat_array(df, keep_spherical_harmonics=False, input_format='nerfstudio'):
    if input_format == 'inria':
        df = rename_inria_columns(df)
    elif input_format == 'nerfstudio':
        df = rename_nerfstudio_columns(df)

    df = convert_data_to_splat(df)
    # analyze_columns(df)
    
    float_cols, uint8_cols, uint8_ranges = splat_columns()
    
    if keep_spherical_harmonics:
        for i in range(16):
            for c in 'rgb':
                float_cols.append('%s_sh%d' % (c, i))
    
    dtypes = [(f, 'float32') for f in float_cols] + [(u, 'uint8') for u in uint8_cols]

    # Create a structured array with the same number of rows as the DataFrame
    structured_array = np.zeros(df.shape[0], dtype=dtypes)

    # Assign the DataFrame columns to the structured array
    for column, dtype in dtypes:
        v = df[column].values
        if dtype == 'uint8':
            v0, v1 = uint8_ranges[column]
            v = np.clip((v - v0)/(v1 - v0) * 0xff, 0, 0xff).astype(np.uint8)
        structured_array[column] = v
    
    flat_array = structured_array.view('uint8')
    return flat_array
    
def dataframe_to_splat_file(df, fn, **kwargs):
    with open(fn, 'wb') as f:
        dataframe_to_flat_array(df, **kwargs).tofile(f)
    
def splat_stream_to_data_frame(input_file):
    float_cols, uint8_cols, uint8_types = splat_columns()
    
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
        
        v0, v1 = uint8_types[c]
        col_uint8 = (packed_col.to_numpy().astype(int) // (2**(sub_idx*8))) % 256
        
        #import matplotlib.pyplot as plt
        #plt.hist(col_uint8, bins=256); plt.title(c); plt.show()
        unpacked_cols[c] = col_uint8 * ((v1 - v0) / 255) + v0
    
    for i in range(n_p):
        df.pop('packed_%d' % i)
    
    for c in uint8_cols:
        df[c] = unpacked_cols[c]
        
    # print(df)

    return df

def splat_file_to_data_frame(input_file):
    with open(input_file, 'rb') as f:
        return splat_stream_to_data_frame(f)
