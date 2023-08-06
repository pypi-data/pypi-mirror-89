from torchvision import datasets
from torch.utils.data import DataLoader
from sitorchtools.imbalanced import ImbalancedDatasetSampler


class FolderLoader(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def loader(self, path, transform, imbalance=False, batch_size=32):

        data_set = datasets.ImageFolder(path, transform=transform)
        if imbalance:
            data_loader = DataLoader(
                data_set,
                sampler=ImbalancedDatasetSampler(data_set),
                batch_size=batch_size
            )
        else:
            data_loader = DataLoader(data_set, batch_size=batch_size, shuffle=True)
        return data_set, data_loader


folder_loader = FolderLoader()
