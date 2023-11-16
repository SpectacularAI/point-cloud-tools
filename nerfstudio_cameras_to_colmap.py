import argparse
import os
import json
import numpy as np
 
def convert_nerfstudio_to_opencv(d):
    def transform_camera(c):
        y_is_up_to_z_is_up = np.array([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0,-1, 0, 0],
            [0, 0, 0, 1]
        ])
    
        convention_change = np.array([
            [1, 0, 0, 0],
            [0,-1, 0, 0],
            [0, 0,-1, 0],
            [0, 0, 0, 1]
        ])
        if len(c) == 3: c.append([0, 0, 0, 1])
        return (y_is_up_to_z_is_up @ np.array(c) @ convention_change).tolist()
        # return np.array(c).tolist()

    unordered = []
    for c in d:
        unordered.append({
            'file_path':  "./images/" + c['file_path'].split('/')[-1],
            "transform": transform_camera(c['transform'])
        })
        
    return sorted(unordered, key=lambda c: c['file_path'])
 
def convert_opencv_to_colmap(cameras, nerfstudio_fake_obs=True):
    from scipy.spatial.transform import Rotation as R

    images = []
    camera_id = 0
    
    positions = []
    for image_id, c in enumerate(cameras):
        positions.append([c['transform'][j][3] for j in range(3)])
        
        mat = np.linalg.inv(np.array(c['transform']))
        qx,qy,qz,qw = R.from_matrix(mat[:3,:3]).as_quat()
        q = [qw, qx, qy, qz]
        p = list(mat[:3, 3])
        images.append([image_id] + list(q) + list(p) + [camera_id, os.path.split(c['file_path'])[-1]])

        points = []
        if nerfstudio_fake_obs:
            points = [100,100,0,200,200,1] # NeRFstudio loader will crash without this

        images.append(points)

    return images, positions
    
def read_colmap_reference(colmap_ref_f):
    unordered = []
    for i, line in enumerate(colmap_ref_f):
        if i % 2 == 0:
            l = line.strip().split(' ')
            for j in range(1, 1 + 7): l[j] = float(l[j])
            unordered.append(l)
    return sorted(unordered, key=lambda c: c[-1])
          
            
def convert_colmap_reference(camera_lines):
    from scipy.spatial.transform import Rotation as R
    for line in camera_lines:
        qw, qx, qy, qz, tx, ty, tz = line[1:(1+7)]
        m = np.eye(4)
        m[:3,:3] = R.from_quat([qx,qy,qz,qw]).as_matrix()
        m[:3, 3] = [tx, ty, tz]
        
        cam_to_world = np.linalg.inv(m)
        pos = list(cam_to_world[:3, 3])
        yield(pos)
        
def realign_poses_in_place(as_opencv, colmap_ref):
    unscaled = np.array([[c['transform'][j][3] for j in range(3)] for c in as_opencv])
    
    mean_unscaled = np.mean(unscaled, axis=0)
    mean_ref = np.mean(colmap_ref, axis=0)
    
    scale = np.linalg.norm(colmap_ref - mean_ref) / np.linalg.norm(unscaled - mean_unscaled)
    
    new_pos = (unscaled - mean_unscaled) * scale + mean_ref
    for i, c in enumerate(as_opencv):
        for j in range(3): c['transform'][j][3] = new_pos[i, j]
       
def read_json(fn):
    with open(fn, 'rt') as f:
        return json.load(f)
        
def write_colmap_csv(data, f):
    for row in data:
        f.write(' '.join([str(c) for c in row])+'\n')

def plot_comparison(colmap_ref, positions):
    import matplotlib.pyplot as plt
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_aspect('equal')
    ax.plot(colmap_ref[:,0], colmap_ref[:,1], colmap_ref[:,2])
    ax.plot(positions[:,0], positions[:, 1], positions[:,2])
    plt.show()

if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description='Nerfstudio camera JSON to COLMAP format')
        parser.add_argument('input_folder', type=str, help='Nerfstudio camera poses export directory')
        parser.add_argument('output_file', type=argparse.FileType('wt'), help='Colmap output file (cameras)')
        parser.add_argument('--colmap_reference', type=argparse.FileType('rt'), help='COLMAP reference file')
        parser.add_argument('--plot', action='store_true')
        parser.add_argument('--include_validation', action='store_true')
        return parser.parse_args()
    
    args = parse_args()
    
    colmap_ref = np.array(list(convert_colmap_reference(read_colmap_reference(args.colmap_reference))))
    
    all_poses = read_json(os.path.join(args.input_folder, 'transforms_train.json'))
    if args.include_validation:
        all_poses.extend(read_json(os.path.join(args.input_folder, 'transforms_eval.json')))
   
    as_opencv = list(convert_nerfstudio_to_opencv(all_poses))
    realign_poses_in_place(as_opencv, colmap_ref)
    as_colmap, positions = convert_opencv_to_colmap(as_opencv)
    
    if args.plot:
        plot_comparison(colmap_ref, np.array(positions))
    
    write_colmap_csv(as_colmap, args.output_file)

