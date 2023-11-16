from formats.auto import load_to_dataframe, save_to_dataframe

if __name__ == '__main__':
    import argparse
    def parse_args():
        parser = argparse.ArgumentParser(description='Gaussian Splatting WebGL renderer "Splat" flat data converter')
        parser.add_argument('input_file', type=str, help='Input file (PLY, Parquet, etc.)')
        parser.add_argument('output_file', type=str, help='Splat output file')
        parser.add_argument('-sh', '--keep_spherical_harmonics', action='store_true')
        parser.add_argument('-f', '--input_format', choices=['inria', 'nerfstudio', 'taichi'], default='nerfstudio')
        return parser.parse_args()
    
    args = parse_args()

    df = load_to_dataframe(args.input_file)
    save_to_dataframe(df, args.output_file, keep_spherical_harmonics=args.keep_spherical_harmonics, input_format=args.input_format)

