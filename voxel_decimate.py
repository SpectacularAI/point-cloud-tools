import pandas as pd
import argparse
   
def voxel_decimate(df, cell_size):
    def grouping_function(row):
        return tuple([round(row[c] / cell_size) for c in 'xyz'])
        
    df['voxel_index'] = df.apply(grouping_function, axis=1)
    grouped = df.groupby('voxel_index')
    return grouped.first().reset_index()
 
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet point cloud converter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='CSV input file')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='CSV output file')
        parser.add_argument('--cell_size', type=float, default=0.1)
        return parser.parse_args()
    
    args = parse_args()

    df = pd.read_csv(args.input_file)
    df = voxel_decimate(df, cell_size=args.cell_size)
    df.to_csv(args.output_file, index=False)

