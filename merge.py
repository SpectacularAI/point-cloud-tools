import pandas as pd
from formats.auto import load_to_dataframe, save_to_dataframe
    
if __name__ == '__main__':
    import argparse
    def parse_args():
        parser = argparse.ArgumentParser(description='Merge point clouds')
        parser.add_argument('input_file', type=str, help='Input file 1')
        parser.add_argument('input_file2', type=str, help='Input file 2')
        parser.add_argument('output_file', type=str, help='Output file')
        return parser.parse_args()
    
    args = parse_args()

    df1 = load_to_dataframe(args.input_file)
    cols = df1.columns
    df2 = load_to_dataframe(args.input_file2)[cols]
    df = pd.concat([df1, df2])
    save_to_dataframe(df, args.output_file)

