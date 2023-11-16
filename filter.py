import numpy as np
import pandas as pd
from formats.auto import load_to_dataframe, save_to_dataframe

def select_sphere(df, origin, radius):
    dist2 = sum([(df[c]-origin[c])**2 for c in 'xyz'])
    return df[dist2 < radius**2]
    
if __name__ == '__main__':
    import argparse
    def parse_args():
        parser = argparse.ArgumentParser(description='Filter point cloud')
        parser.add_argument('input_file', type=str, help='Input file 1')
        parser.add_argument('output_file', type=str, help='Output file')
        parser.add_argument('-x', type=float, default=0)
        parser.add_argument('-y', type=float, default=0)
        parser.add_argument('-z', type=float, default=0)
        parser.add_argument('-r', '--radius', type=float, default=1)
        return parser.parse_args()
    
    args = parse_args()
    df = load_to_dataframe(args.input_file)
    df = select_sphere(df, origin={'x': args.x, 'y': args.y, 'z': args.z}, radius=args.radius)
    save_to_dataframe(df, args.output_file)

