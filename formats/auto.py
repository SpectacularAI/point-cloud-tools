import pandas as pd

from .ply import load_ply_to_dataframe, dataframe_to_ply
from .splat import splat_file_to_data_frame, dataframe_to_splat_file
from .pcd import dataframe_to_pcd
from .html import dataframe_to_gsplat_html

def load_to_dataframe(fn):
    ext = fn.split('.')[-1]
    
    if ext == 'ply':
        return load_ply_to_dataframe(fn)
    elif ext == 'csv':
        return pd.read_csv(fn)
    elif ext == 'txt':
        # assuming COLMAP CSV format
        return pd.read_csv(fn, sep=' ', header=None, usecols=list(range(7)), names=['id'] + list('xyzrgb')).set_index('id')
    elif ext == 'parquet':
        return pd.read_parquet(fn)
    elif ext == 'splat':
        return splat_file_to_data_frame(fn)
    elif ext == 'pcd':
        raise RuntimeError("PCD import not implemented")
    else:
        raise RuntimeError("unrecognized extension ." + ext)
        
def save_to_dataframe(df, fn, args):
    ext = fn.split('.')[-1]
    
    if ext == 'ply':
        dataframe_to_ply(df, fn)
    elif ext == 'csv':
        return df.to_csv(fn, index=False)
    elif ext == 'parquet':
        return df.to_parquet(fn)
    elif ext == 'splat':
        return dataframe_to_splat_file(df, fn, input_format=args.ply_input_format)
    elif ext == 'pcd':
        return dataframe_to_pcd(df, fn) # TODO: kwargs
    elif ext == 'html':
        return dataframe_to_gsplat_html(df, fn,
            input_format=args.ply_input_format,
            html_template=args.html_template)
    elif ext == 'ply':
        raise RuntimeError("PLY export not implemented")
    else:
        raise RuntimeError("unrecognized extension ." + ext)
