import pandas as pd
import argparse

if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='CSV to parquet point cloud converter')
        parser.add_argument('input_file', type=argparse.FileType('rt'), help='CSV input file')
        parser.add_argument('output_file', type=argparse.FileType('wb'), help='Parquet output file')
        return parser.parse_args()
    
    args = parse_args()
    df = pd.read_csv(args.input_file)
    df.to_parquet(args.output_file)

