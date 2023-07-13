import os
import pandas as pd
import numpy as np


def get_t_camera_radar(dataset_path, frame):
    with open(os.path.join(dataset_path, 'calib', f"{frame}.txt"), "r") as f:
        lines = f.readlines()
        matrix = np.array(lines[0].strip().split(' ')[1:], dtype=np.float32).reshape(4, 4)

    return matrix


def get_camera_projection_matrix(dataset_path, frame):
    with open(os.path.join(dataset_path, 'calib', f"{frame}.txt"), "r") as f:
        lines = f.readlines()
        matrix = np.array(lines[1].strip().split(' ')[1:], dtype=np.float32).reshape(3, 4)

    return matrix


def project_pcl_to_image(pcl, t_camera_radar, camera_projection_matrix):
    location = np.hstack((pcl[['x', 'y', 'z']],
                          np.ones((pcl.shape[0], 1))))
    print('location', location)
    radar_points_camera_frame = t_camera_radar.dot(location.T).T
    print('radar_points_camera_frame', radar_points_camera_frame)

    return project_3d_to_2d(radar_points_camera_frame, camera_projection_matrix)


def project_3d_to_2d(points: np.ndarray, projection_matrix: np.ndarray):
    if points.shape[-1] != 4:
        raise ValueError(f"{points.shape[-1]} must be 4!")

    uvw = projection_matrix.dot(points.T)
    print('uvw', uvw)
    uvw /= uvw[2]



    uvs = uvw[:2].T
    print('uvs', uvs)
    uvs = np.round(uvs).astype(np.int32)

    return uvs


if __name__ == '__main__':
    dataset_path = "/data/waterscenes/all"
    frame = '1664246698.44130'

    # Get radar data
    radar = pd.read_csv(os.path.join(dataset_path, 'radar', f'{frame}.csv'))
    print(radar[['x', 'y', 'z', 'u', 'v']])

    # Get intrinsic and extrinsic
    t_camera_radar = get_t_camera_radar(dataset_path, frame)
    print(t_camera_radar)
    camera_projection_matrix = get_camera_projection_matrix(dataset_path, frame)
    print(camera_projection_matrix)

    # Transform pcl to uvs
    uvs = project_pcl_to_image(radar, t_camera_radar, camera_projection_matrix)
    print(uvs)
