import pandas as pd
import numpy as np
import struct
import re

# mostly ChatGPT-generated
def parse_ply_header(ply_file):
    property_pattern = re.compile(rb'property (\w+) (\w+)')
    header = {
        'format': 'ascii',
        'properties': [],
        'vertex_count': 0
    }
    while True:
        line = ply_file.readline().strip()
        if line == b"end_header":
            break
        elif line.startswith(b"element vertex"):
            header['vertex_count'] = int(line.split()[-1])
        elif line.startswith(b"format"):
            header['format'] = line.split()[1].decode('ascii')
        elif property_pattern.match(line):
            property_type, property_name = property_pattern.findall(line)[0]
            header['properties'].append((property_name.decode('ascii'), property_type.decode('ascii')))
            
    return header
    
PLY_TYPE_MAPPING = {
    'float': 'f',
    'double': 'd',
    'int': 'i',
    'uint8': 'B',
    'uchar': 'B',
    'char': 'b',
    'uint': 'I',
    'ushort': 'H',
    'short': 'h'
}
 
def read_binary_ply_data(ply_file, header):
    endian_char = '<' if header['format'] == 'binary_little_endian' else '>'
    format_string = endian_char + ''.join(PLY_TYPE_MAPPING[ptype] for pname, ptype in header['properties'])
    vertex_size = struct.calcsize(format_string)
    vertices = [
        struct.unpack(format_string, ply_file.read(vertex_size))
        for _ in range(header['vertex_count'])
    ]
    dtypes = [(pname, PLY_TYPE_MAPPING[ptype]) for pname, ptype in header['properties']]
    structured_array = np.array(vertices, dtype=dtypes)
    
    return structured_array
   
def read_ascii_ply_data(ply_file, header):    
    dtypes = [(pname, PLY_TYPE_MAPPING[ptype]) for pname, ptype in header['properties']]
    
    vertices = []
    
    for _ in range(header['vertex_count']):
        line = ply_file.readline().strip()
        values = line.split()
        vertex = tuple([float(v.decode('ascii')) for v in values]) # hacky
        vertices.append(vertex)
    
    structured_array = np.array(vertices, dtype=dtypes)
    return structured_array
    
def load_ply_stream_to_dataframe(ply_file):
    header = parse_ply_header(ply_file)
    # print(header)
    
    if header['format'] in ['binary_little_endian', 'binary_big_endian']:
        structured_array = read_binary_ply_data(ply_file, header)
    elif header['format'] == 'ascii':
        structured_array = read_ascii_ply_data(ply_file, header)
    else:
        raise ValueError('invalid PLY header format')
    df = pd.DataFrame(structured_array)
    return df

def load_ply_to_dataframe(ply_file):
    with open(ply_file, 'rb') as f:
        return load_ply_stream_to_dataframe(f)
    load_ply_to_dataframe
    

def generate_ply_header(df):
    header = "ply\nformat binary_little_endian 1.0\n"
    header += f"element vertex {len(df)}\n"
    for column in df.columns:
        header += f"property float {column}\n"

    header += "end_header\n"
    return header

def dataframe_to_ply(df, output_file):
    header = generate_ply_header(df)

    with open(output_file, 'wb') as f:
        f.write(header.encode())
        for _, row in df.iterrows():
            for column in df.columns:
                f.write(struct.pack('f', row[column]))

