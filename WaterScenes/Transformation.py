import numpy as np


def project_pcl_to_image(pcl, t_camera_radar, camera_projection_matrix, image_shape):
    location = np.hstack((pcl[['x', 'y', 'z']],
                          np.ones((pcl.shape[0], 1))))
    # print(location)

    radar_points_camera_frame = t_camera_radar.dot(location.T).T

    point_depth = radar_points_camera_frame[:, 2]

    uvs = project_3d_to_2d(radar_points_camera_frame, camera_projection_matrix)
    power = pcl['rcs']

    return uvs, point_depth, power, pcl


def project_3d_to_2d(points: np.ndarray, projection_matrix: np.ndarray):
    """
This function projects the input 3d ndarray to a 2d ndarray, given a projection matrix.
    :param points: Homogenous points to be projected.
    :param projection_matrix: 4x4 projection matrix.
    :return: 2d ndarray of the projected points.
    """
    if points.shape[-1] != 4:
        raise ValueError(f"{points.shape[-1]} must be 4!")

    uvw = projection_matrix.dot(points.T)
    uvw /= uvw[2]
    uvs = uvw[:2].T
    uvs = np.round(uvs).astype(np.int)

    return uvs


def canvas_crop(points, image_size, pcl, points_depth=None):
    """
This function filters points that lie outside a given frame size.
    :param power:
    :param points: Input points to be filtered.
    :param image_siz e: Size of the frame.
    :param points_depth: Filters also depths smaller than 0.
    :return: Filtered points.
    """
    idx = points[:, 0] > 0
    idx = np.logical_and(idx, points[:, 0] < image_size[1])
    idx = np.logical_and(idx, points[:, 1] > 0)
    idx = np.logical_and(idx, points[:, 1] < image_size[0])
    idx = np.logical_and(idx, pcl[:, 3] > 0)

    # tmp
    # idx = np.logical_and(idx, pcl[:, 1] < -7)
    if points_depth is not None:
        idx = np.logical_and(idx, points_depth > 0)

    return idx
