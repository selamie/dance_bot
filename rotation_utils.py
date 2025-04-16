import numpy as np

def quaternion_to_rotation_matrix(q):
    # Extract quaternion components from the 1x4 array
    qx, qy, qz, qw = q
    
    R = np.array([
        [1 - 2*(qy**2 + qz**2), 2*(qx*qy - qw*qz), 2*(qx*qz + qw*qy)],
        [2*(qx*qy + qw*qz), 1 - 2*(qx**2 + qz**2), 2*(qy*qz - qw*qx)],
        [2*(qx*qz - qw*qy), 2*(qy*qz + qw*qx), 1 - 2*(qx**2 + qy**2)]
    ])
    
    return R

def apply_xrot(rad,pose):
    xrot = np.array([[1,0,0],[0,np.cos(rad),-np.sin(rad)],[0,np.sin(rad),np.cos(rad)]])
    new = pose@xrot

    return new

def apply_yrot(rad, pose):
    yrot = np.array([
        [np.cos(rad), 0, np.sin(rad)],
        [0, 1, 0],
        [-np.sin(rad), 0, np.cos(rad)]
    ])
    new = pose @ yrot
    return new


def apply_zrot(rad, pose):
    zrot = np.array([
        [np.cos(rad), -np.sin(rad), 0],
        [np.sin(rad), np.cos(rad), 0],
        [0, 0, 1]
    ])
    new = pose @ zrot
    return new

def generate_rotation_array(n,degs):
    angles_deg = np.random.uniform(-degs, degs, size=n)
    angles_rad = np.deg2rad(angles_deg)
    
    axes = np.random.choice(['x', 'y', 'z'], size=n)

    result = np.empty((n, 2), dtype=object)
    result[:, 0] = angles_rad
    result[:, 1] = axes

    return result
