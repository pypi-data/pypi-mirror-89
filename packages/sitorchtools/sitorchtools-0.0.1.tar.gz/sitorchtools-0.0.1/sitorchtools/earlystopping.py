import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import classification_report
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")


class EarlyStopping:
    """
    This script was modify from https://github.com/Bjarten/early-stopping-pytorch.
    Early stops the training if validation loss doesn"t improve after a given patience.
    """

    def __init__(self, patience=7, verbose=True, delta=0, path="best_model.pth", trace_func=print, model_class=None):
        """
        Args:
            patience (int): How long to wait after last time validation loss improved.
                            Default: 7
            verbose (bool): If True, prints a message for each validation loss improvement.
                            Default: False
            delta (float): Minimum change in the monitored quantity to qualify as an improvement.
                            Default: 0
            path (str): Path for the checkpoint to be saved to.
                            Default: "checkpoint.pt"
            trace_func (function): trace print function.
                            Default: print
        """
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.path = path
        self.trace_func = trace_func
        self.model_class = model_class
        self.epoch = 1
        self.train_losses = []
        self.val_losses = []

    def __call__(self, model, train_loss, val_loss, y_true=None, y_pred=None, plot=False):

        score = -val_loss
        self.trace_func(f"Epoch: {self.epoch}")
        self.trace_func(f"Train Loss: {train_loss} | Validation Loss: {val_loss}")
        self.train_losses.append(train_loss)
        self.val_losses.append(val_loss)
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, y_true, y_pred)
        elif score < self.best_score + self.delta:
            self.counter += 1
            self.trace_func(f"EarlyStopping counter: {self.counter} out of {self.patience}")
            if self.counter >= self.patience:
                self.early_stop = True
                self.plotting(self.train_losses, self.val_losses, plot)
                self.trace_func(f"Best Model Report:\n{self.load_best_performance()}")
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model, y_true, y_pred)
            self.counter = 0
        self.epoch += 1

    def save_checkpoint(self, val_loss, model, y_true, y_pred):
        """Saves model when validation loss decrease."""
        checkpoint = {
            "state_dict": model.state_dict()
        }
        if self.verbose:
            self.trace_func(f"Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...")
        if y_true and y_pred:
            checkpoint["performance"] = classification_report(y_true, y_pred, output_dict=False)
        if self.model_class:
            checkpoint["model"] = self.model_class
        torch.save(checkpoint, self.path)
        self.val_loss_min = val_loss

    def reset_early_stop(self):
        self.counter = 0
        self.early_stop = False

    def plotting(self, train_loss, valid_loss, plot=False):
        fig = plt.figure(figsize=(10, 8))
        plt.plot(range(1, len(train_loss) + 1), train_loss, label="Training Loss")
        plt.plot(range(1, len(valid_loss) + 1), valid_loss, label="Validation Loss")
        # find position of lowest validation loss
        minposs = valid_loss.index(min(valid_loss)) + 1
        plt.axvline(minposs, linestyle="--", color="r", label="Early Stopping Checkpoint")
        plt.xlabel("epochs")
        plt.ylabel("loss")
        plt.ylim(0, 1)
        plt.xlim(0, len(train_loss) + 1)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        if plot:
            plt.show()
        fig.savefig("loss_plot.png", bbox_inches="tight")

    def load_best_performance(self):
        checkpoint = torch.load(self.path)
        if checkpoint.get("performance", None):
            model = checkpoint["performance"]
        else:
            model = None
        return model
