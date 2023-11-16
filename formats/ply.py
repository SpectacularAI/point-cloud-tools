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
 
def read_binary_ply_data(ply_file, header):
    type_mapping = {
        'float': 'f',
        'double': 'd',
        'int': 'i',
        'uchar': 'B',
        'char': 'b',
        'uint': 'I',
        'ushort': 'H',
        'short': 'h'
    }
    endian_char = '<' if header['format'] == 'binary_little_endian' else '>'
    format_string = endian_char + ''.join(type_mapping[ptype] for pname, ptype in header['properties'])
    vertex_size = struct.calcsize(format_string)
    vertices = [
        struct.unpack(format_string, ply_file.read(vertex_size))
        for _ in range(header['vertex_count'])
    ]
    dtypes = [(pname, type_mapping[ptype]) for pname, ptype in header['properties']]
    structured_array = np.array(vertices, dtype=dtypes)
    
    return structured_array
    
def load_ply_stream_to_dataframe(ply_file):
    header = parse_ply_header(ply_file)
    # print(header)
    if header['format'] != 'binary_little_endian' and header['format'] != 'binary_big_endian':
        raise ValueError('PLY file is not in binary format.')
    structured_array = read_binary_ply_data(ply_file, header)
    df = pd.DataFrame(structured_array)
    return df

def load_ply_to_dataframe(ply_file):
    with open(ply_file, 'rb') as f:
        return load_ply_stream_to_dataframe(f)
    load_ply_to_dataframe
