import pandas as pd
import argparse
    
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet point cloud converter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='CSV input file')
        parser.add_argument('input_file2', type=argparse.FileType('rb'), help='CSV input file')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='CSV output file')
        return parser.parse_args()
    
    args = parse_args()

    df1 = pd.read_csv(args.input_file, usecols=['x','y','z'])
    df2 = pd.read_csv(args.input_file2, usecols=['x','y','z'])
    df = pd.concat([df1, df2])
    df.to_csv(args.output_file, index=False)

