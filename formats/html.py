import os
import numpy as np
import base64
import gzip
import io
import math

from .splat import dataframe_to_flat_array

def quat_rot_from_A_to_B(A, B):
    A_norm = np.array(A) / np.linalg.norm(A)
    B_norm = np.array(B) / np.linalg.norm(B)
    # Compute the cross product and angle
    cross_prod = np.cross(A_norm, B_norm)
    dot_prod = np.dot(A_norm, B_norm)
    angle = np.arccos(dot_prod)
    # Compute the quaternion
    sin_half_angle = np.sin(angle / 2)
    cn = np.linalg.norm(cross_prod)
    if abs(cn) < 1e-6: return [1, 0, 0, 0]
    rotation_axis = cross_prod / cn
    return np.array([
        np.cos(angle / 2),
        rotation_axis[0] * sin_half_angle,
        rotation_axis[1] * sin_half_angle,
        rotation_axis[2] * sin_half_angle
    ])

HTML_TEMPLATE = '../gsplat.js.html.template'
def dataframe_to_gsplat_html(df, fn, scene_up_direction, **kwargs):
    template_path = os.path.join(os.path.dirname(__file__), HTML_TEMPLATE)
    with open(template_path, 'rt') as f:
        html_template = f.read()
    
    splat_data = dataframe_to_flat_array(df, **kwargs)
    UP_DIR_TARGET = [0, 0, 1] # z-is-up
    
    up_dir = [float(c) for c in scene_up_direction.split(',')]
    qw, qx, qy, qz = quat_rot_from_A_to_B(up_dir, UP_DIR_TARGET)
    
    q = ', '.join([str(c) for c in [qx, qy, qz, qw]]) # wxyz -> xyzw
    html = html_template.replace('SCENE_ROTATION_QUAT', q).replace('CORS_SUCKS', base64.b64encode(splat_data.tobytes()).decode('utf-8'))
    
    with open(fn, 'wt') as f:
        f.write(html)
