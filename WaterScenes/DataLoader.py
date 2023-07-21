from matplotlib import pyplot as plt
import os
import numpy as np
import pandas as pd


class DataLoader:
    def __init__(self, dataset_path, frame):
        self.dataset_path = dataset_path
        self.frame = frame

    @property
    def image(self):
        return self.get_image()

    @property
    def radar_data(self):
        return self.get_radar_data()

    @property
    def radar_3_frames_data(self):
        return self.get_radar_3_frames_data()

    @property
    def label_data(self):
        return self.get_label_data()

    @property
    def t_camera_radar(self):
        return self.get_t_camera_radar()

    @property
    def camera_projection_matrix(self):
        return self.get_camera_projection_matrix()

    def get_label_data(self):
        labels = []
        f = open(os.path.join(self.dataset_path, 'detection/yolo', f'{self.frame}.txt'))
        for line in f.readlines():
            width = 1920
            height = 1080
            label_class, x, y, w, h = line.split()
            label_class = int(label_class)
            x = float(x)
            y = float(y)
            w = float(w)
            h = float(h)
            xmin = int(width * (x - 0.5 * w))
            ymin = int(height * (y - 0.5 * h))
            xmax = int(width * (x + 0.5 * w))
            ymax = int(height * (y + 0.5 * h))

            labels.append({'class': label_class,
                           'xmin': xmin,
                           'ymin': ymin,
                           'xmax': xmax,
                           'ymax': ymax}
                          )
        return labels

    def get_image(self):
        return plt.imread(os.path.join(self.dataset_path, 'image', f'{self.frame}.jpg'))

    def get_radar_data(self):
        return pd.read_csv(os.path.join(self.dataset_path, 'radar', f'{self.frame}.csv'))

    def get_radar_3_frames_data(self):
        return pd.read_csv(os.path.join(self.dataset_path, 'radar_3_frames', f'{self.frame}.csv'))

    def get_t_camera_radar(self):
        with open(os.path.join(self.dataset_path, 'calib', f"{self.frame}.txt"), "r") as f:
            lines = f.readlines()
            matrix = np.array(lines[0].strip().split(' ')[1:], dtype=np.float32).reshape(4, 4)

        return matrix

    def get_camera_projection_matrix(self):
        with open(os.path.join(self.dataset_path, 'calib', f"{self.frame}.txt"), "r") as f:
            lines = f.readlines()
            matrix = np.array(lines[1].strip().split(' ')[1:], dtype=np.float32).reshape(3, 4)

        return matrix
