import pandas as pd
import argparse
from scipy.spatial import KDTree
   
def interpolate_missing_properties(df_source, df_query, k_nearest=3):
    xyz = list('xyz')

    tree = KDTree(df_source[xyz].values)
    _, ii = tree.query(df_query[xyz], k=k_nearest)
    n = df_query.shape[0]
    
    df_result = pd.DataFrame(0, index=range(n), columns=df_source.columns)
    df_result[xyz] = df_query[xyz]
    other_cols = [c for c in df_source.columns if c not in xyz]
   
    for i in range(n):
        m = df_source.loc[ii[i].tolist(), other_cols].mean(axis=0)
        df_result.loc[i, other_cols] = m
    
    return df_result
 
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet point cloud converter')
        parser.add_argument('input_source_file', type=argparse.FileType('rb'), help='CSV input file: search')
        parser.add_argument('input_query_file', type=argparse.FileType('rb'), help='CSV input file: query')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='CSV output file')
        return parser.parse_args()
    
    args = parse_args()

    df1 = pd.read_csv(args.input_source_file)
    df2 = pd.read_csv(args.input_query_file, usecols=['x','y','z'])
    df3 = interpolate_missing_properties(df1, df2)
    df3.to_csv(args.output_file, index=False)

