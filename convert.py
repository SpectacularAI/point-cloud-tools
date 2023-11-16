from formats.auto import load_to_dataframe, save_to_dataframe

if __name__ == '__main__':
    import argparse
    def parse_args():
        parser = argparse.ArgumentParser(description='Point cloud converter')
        parser.add_argument('input_file', type=str, help='Input file')
        parser.add_argument('output_file', type=str, nargs='?', default=None, help='Output file')
        return parser.parse_args()
    
    args = parse_args()
    
    df = load_to_dataframe(args.input_file)
    if args.output_file is None:
        print(df)
    else:
        save_to_dataframe(df, args.output_file)

