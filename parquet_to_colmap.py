import pandas as pd
import argparse
 
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet point cloud to COLMAP sparse point format converter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='Parquet input file')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='Colmap output file')
        parser.add_argument('--binary', action='store_true')
        return parser.parse_args()
    
    args = parse_args()
    if args.binary: raise RuntimeError("TODO")

    df = pd.read_parquet(args.input_file)
    cols = [c for c in df.columns if c in 'xyzrgb']
    df[cols].to_csv(args.output_file, index=False, header=False, sep=' ')

