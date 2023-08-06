import shutil
import os
import numpy as np


class ImgFolderSplit(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_files_from_folder(self, path):
        files = os.listdir(path)
        return np.asarray(files)

    def split_folder(self, path_to_train_data, path_to_test_data, train_ratio):
        """split_folder

        Args:
            path_to_train_data ([str]): [path to train data ex: data/train]
            path_to_test_data ([str]): [path to test data ex: data/test]
            train_ratio ([float]): train ratio
        """
        _, dirs, _ = next(os.walk(path_to_train_data))
        # calculates how many train data per class
        data_counter_per_class = np.zeros((len(dirs)))
        for i in range(len(dirs)):
            path = os.path.join(path_to_train_data, dirs[i])
            files = self.get_files_from_folder(path)
            data_counter_per_class[i] = len(files)
        test_counter = np.round(data_counter_per_class * (1 - train_ratio))
        # transfers files
        for i in range(len(dirs)):
            path_to_original = os.path.join(path_to_train_data, dirs[i])
            path_to_save = os.path.join(path_to_test_data, dirs[i])
            # creates dir
            if not os.path.exists(path_to_save):
                os.makedirs(path_to_save)
            files = self.get_files_from_folder(path_to_original)
            # moves data
            for j in range(int(test_counter[i])):
                dst = os.path.join(path_to_save, files[j])
                src = os.path.join(path_to_original, files[j])
                shutil.move(src, dst)


img_folder_split = ImgFolderSplit()
