import numpy as np
import pandas as pd
import argparse

def select_sphere(df, origin, radius):
    dist2 = sum([(df[c]-origin[c])**2 for c in 'xyz'])
    return df[dist2 < radius**2]
    
if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Parquet filter')
        parser.add_argument('input_file', type=argparse.FileType('rb'), help='Parquet input file')
        parser.add_argument('output_file', type=argparse.FileType('wb'), help='Parquet output file')
        parser.add_argument('-x', type=float, default=0)
        parser.add_argument('-y', type=float, default=0)
        parser.add_argument('-z', type=float, default=0)
        parser.add_argument('-r', '--radius', type=float, default=1)
        return parser.parse_args()
    
    args = parse_args()
    df = pd.read_parquet(args.input_file)
    df = select_sphere(df, origin={'x': args.x, 'y': args.y, 'z': args.z}, radius=args.radius)
    df.to_parquet(args.output_file)

