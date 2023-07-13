
from WaterScenes.DataLoader import DataLoader
from WaterScenes.Visualization import Visualization

# from DataLoader import DataLoader
# from Visualization import Visualization

class WaterScenes:

    def __init__(self, dataset_path=None):
        self.dataset_path = dataset_path

    def visualization(self, frame, show_labels=False, show_radar_label=False, show_radar=True, plot_figure=True, save_figure=True):
        visualization = Visualization(DataLoader(self.dataset_path, frame))
        visualization.plot(show_labels, show_radar_label, show_radar, plot_figure, save_figure)


# if __name__ == '__main__':
#     dataset_path = "/data/waterscenes/date/test"
#     waterscenes = WaterScenes(dataset_path)
#
#
#     frame = '1664246698.44130'
#     waterscenes.visualization(frame)
