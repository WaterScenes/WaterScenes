from matplotlib import pyplot as plt
from WaterScenes.Transformation import project_pcl_to_image
from WaterScenes.Config import label_color, label_code

import os

class Visualization:
    def __init__(self, dataloader):
        self.dataloader = dataloader

    def plot(self, show_labels=False,
             show_radar_label=False,
             show_radar=False,
             plot_figure=False,
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
        # radar = radar.append({'u': -1, 'v': -1, 'range': 100, 'rcs': 1}, ignore_index=True)
        power = radar['rcs']
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
        idx = radar['label'] != 0
        uvs = radar[idx]
        plt.scatter(uvs['u'], uvs['v'], alpha=0.8, cmap='jet', marker="*")
