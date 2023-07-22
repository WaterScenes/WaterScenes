from WaterScenes.DataLoader import DataLoader
from matplotlib import pyplot as plt
from WaterScenes.Transformation import project_pcl_to_image
from WaterScenes.Config import label_color, label_code
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class WaterScenes:

    def __init__(self, dataset_path=None, frame=''):
        self.dataset_path = dataset_path
        self.dataloader = DataLoader(self.dataset_path, frame)

    def visualization(self, show_labels=False,
                      show_radar_label=False,
                      show_radar=False,
                      plot_figure=True,
                      save_figure=False):
        fig = plt.figure(figsize=(19.2, 10.8))
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        plt.clf()
        fig.set_dpi(100)

        if show_labels:
            self.plot_gt_labels()

        if show_radar:
            self.plot_radar_pcl()
            # self.plot_radar_pcl_from_calibration()

        if show_radar_label:
            self.plot_radar_label()

        plt.imshow(self.dataloader.image, alpha=1)
        # plt.colorbar()
        plt.axis('off')

        if save_figure:
            visualization_path = 'visualization'
            if not os.path.exists(visualization_path):
                os.mkdir(visualization_path)
            plt.savefig(visualization_path + f'/{self.dataloader.frame}.png')

        if plot_figure:
            plt.show()

        plt.close(fig)

        return

    def plot_boxes(self, locations, color):
        x1 = locations[0]
        x2 = locations[2]
        y1 = locations[1]
        y2 = locations[3]

        plt.plot([x1, x1], [y1, y2], color=color)
        plt.plot([x1, x2], [y1, y1], color=color)
        plt.plot([x2, x2], [y1, y2], color=color)
        plt.plot([x1, x2], [y2, y2], color=color)

    def plot_gt_labels(self):
        gt_labels = self.dataloader.get_label_data()
        for gt_label in gt_labels:
            self.plot_boxes([gt_label['xmin'], gt_label['ymax'], gt_label['xmax'], gt_label['ymin']],
                            label_color[gt_label['class']])

    def plot_radar_pcl(self):

        radar = self.dataloader.radar_data
        # radar = radar.append({'u': -1, 'v': -1, 'range': 100, 'power': 1}, ignore_index=True)
        power = radar['power']
        points_depth = radar['range']

        plt.scatter(radar['u'], radar['v'], c=-points_depth, s=power * power, alpha=0.8, cmap='jet')

    def plot_radar_pcl_from_calibration(self):
        uvs, points_depth, power, _ = project_pcl_to_image(self.dataloader.radar_data,
                                                           self.dataloader.t_camera_radar,
                                                           self.dataloader.camera_projection_matrix,
                                                           self.dataloader.image.shape)

        plt.scatter(uvs[:, 0], uvs[:, 1], c=-points_depth, alpha=0.8, cmap='jet')

    def plot_radar_label(self):
        radar = self.dataloader.radar_data
        idx = radar['label'] != -1
        uvs = radar[idx]
        plt.scatter(uvs['u'], uvs['v'], alpha=0.8, marker="*")

    def visualization3D(self, frames=1, coordinate='Cartesian'):

        if frames == 1:
            radar = self.dataloader.radar_data
            labels = np.array(radar[['label']]).squeeze(1)
            labels_3D = ['r' if c > -1 else 'b' for c in labels]

        if frames == 3:
            radar = self.dataloader.radar_3_frames_data

            # No labels for radar_3_frames
            labels_3D = ['b']

        fig = plt.figure(dpi=200)
        # ax = Axes3D(fig)
        ax = fig.add_subplot(projection='3d')

        if coordinate == 'Cartesian':
            ax.scatter(radar[['x']], radar[['y']], radar[['z']],
                       # cmap='spectral',
                       s=radar[['power']],
                       linewidth=0,
                       alpha=1,
                       marker=".",
                       c=labels_3D)
            ax.set_xlabel('X', fontsize=8, fontweight='bold')
            ax.set_ylabel('Y', fontsize=8, fontweight='bold')
            ax.set_zlabel('Z', fontsize=8, fontweight='bold')

        if coordinate == 'World':
            ax.scatter(radar[['x']], radar[['z']], -radar[['y']],
                       # cmap='spectral',
                       s=radar[['power']],
                       linewidth=0,
                       alpha=1,
                       marker=".",
                       c=labels_3D)
            ax.set_xlabel('X', fontsize=8, fontweight='bold')
            ax.set_ylabel('Z', fontsize=8, fontweight='bold')
            ax.set_zlabel('Y', fontsize=8, fontweight='bold')

        plt.show()
