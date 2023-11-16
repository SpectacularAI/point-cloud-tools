import pandas as pd
from scipy.spatial import KDTree
from formats.auto import load_to_dataframe, save_to_dataframe
   
def exclude_points(df_source, df_exclude, radius):
    xyz = list('xyz')

    tree = KDTree(df_exclude[xyz].values)
    ii = tree.query_ball_point(df_source[xyz], r=radius, return_length=True)
   
    mask = [l == 0 for l in ii]
    df_result = df_source.iloc[mask]
    
    return df_result
 
if __name__ == '__main__':
    import argparse
    def parse_args():
        parser = argparse.ArgumentParser(description='Exclude points near another point cloud')
        parser.add_argument('input_source_file', type=str, help='Input file: search')
        parser.add_argument('input_exclude_file', type=str, help='Input file: exclude')
        parser.add_argument('output_file', type=str, help='Output file')
        parser.add_argument('--radius', type=float)
        return parser.parse_args()
    
    args = parse_args()

    df1 = load_to_dataframe(args.input_source_file)
    df2 = load_to_dataframe(args.input_exclude_file)[['x','y','z']]
    df3 = exclude_points(df1, df2, args.radius)
    save_to_dataframe(df3, args.output_file)

