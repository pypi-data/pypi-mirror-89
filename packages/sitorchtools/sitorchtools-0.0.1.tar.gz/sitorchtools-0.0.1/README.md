# sitorchtools
Support function for train dataset using Pytorch

## Features
```
Early Stopping based on validation loss
Folder loader based on pytorch DataLoader
Imblanaced image data handling
Spliting Image on Folder to train and test dataset
```
## Usage
1. EarlyStopping
```
from sitorchtools import EarlyStopping, folder_loader, img_folder_split
    early_stopping = EarlyStopping(
        patience=7,
        verbose=True,
        delta=0,
        path="best_model.pth",
        trace_func=print,
        model_class=None
        )

    early_stopping(model, train_loss, valid_loss, y_true, y_pred, plot=False)
```

2. Data Loader
```
train_set, train_loader = folder_loader.loader(
    your_train_path,
    transform=your_train_transform,
    batch_size=your_bs,
    imbalance=True)
```

3. image folder split
```
img_folder_split.split_folder(path_to_train_data, path_to_test_data, train_ratio)
```
