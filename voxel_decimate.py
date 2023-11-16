import pandas as pd
from formats.auto import load_to_dataframe, save_to_dataframe
   
def voxel_decimate(df, cell_size):
    def grouping_function(row):
        return tuple([round(row[c] / cell_size) for c in 'xyz'])
        
    df['voxel_index'] = df.apply(grouping_function, axis=1)
    grouped = df.groupby('voxel_index')
    return grouped.first().reset_index()
 
if __name__ == '__main__':
    import argparse
    
    def parse_args():
        parser = argparse.ArgumentParser(description='Voxel-decimation point cloud')
        parser.add_argument('input_file', type=str, help='Input file')
        parser.add_argument('output_file', type=str, help='Output file')
        parser.add_argument('--exclude_file', type=str, default=None, help='Exclude points in same voxels with these')
        parser.add_argument('--cell_size', type=float, default=0.1)
        return parser.parse_args()
    
    args = parse_args()

    df = load_to_dataframe(args.input_file)
    df = voxel_decimate(df, cell_size=args.cell_size)
    save_to_dataframe(df, args.output_file)

