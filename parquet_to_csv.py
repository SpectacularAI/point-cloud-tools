import pandas as pd
import argparse
 
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet point cloud to CSV converter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='Parquet input file')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='CSV output file')
        parser.add_argument('--columns', type=str, default=None)
        return parser.parse_args()
    
    args = parse_args()


    df = pd.read_parquet(args.input_file)
    if args.columns is not None:
        df = df[args.columns.split(',')]
    df.to_csv(args.output_file, index=False)

