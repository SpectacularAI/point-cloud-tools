import pandas as pd
import argparse
from scipy.spatial import KDTree
   
def exclude_points(df_source, df_exclude, radius):
    xyz = list('xyz')

    tree = KDTree(df_exclude[xyz].values)
    ii = tree.query_ball_point(df_source[xyz], r=radius, return_length=True)
   
    mask = [l == 0 for l in ii]
    df_result = df_source.iloc[mask]
    
    return df_result
 
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet point cloud converter')
        parser.add_argument('input_source_file', type=argparse.FileType('rb'), help='CSV input file: search')
        parser.add_argument('input_exclude_file', type=argparse.FileType('rb'), help='CSV input file: exclude points near these')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='CSV output file')
        parser.add_argument('--radius', type=float)
        return parser.parse_args()
    
    args = parse_args()

    df1 = pd.read_csv(args.input_source_file)
    df2 = pd.read_csv(args.input_exclude_file, usecols=['x','y','z'])
    df3 = exclude_points(df1, df2, args.radius)
    df3.to_csv(args.output_file, index=False)

