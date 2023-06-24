import torch.nn  as nn
import numpy as np
import torch
import sys
sys.path.append("../datasets")
sys.path.append("../model")
from torch.nn import functional as F
# Convnext

# import data
# import utils
import backbone
import matplotlib.pyplot as plt
plt.style.use('ggplot')

class SaveBestModel:
    # this class only work for each training
    """
    Class to save the best model while training. If the current epoch's 
    validation loss is less than the previous least less, then save the
    model state.
    """
    def __init__(
        self, best_valid_AUC=float('inf')
    ):
        self.best_valid_AUC = best_valid_AUC
        
    def __call__(
        self, metric, 
        epoch, model, optimizer, criterion
    ):
        if metric.meanAUC < self.best_valid_loss:
            self.best_valid_AUC= metric.meanAUC
            print(f"\nBest validation  AUC: {self.best_valid_AUC}")
            print(f"\nSaving best model for epoch: {epoch+1}\n")
            torch.save({
                'epoch': epoch+1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': criterion,
                }, 'output/best_model.pth')



def save_plots(train_acc, valid_acc, train_loss, valid_loss):
    """
    Function to save the loss and accuracy plots to disk.
    """
    # accuracy plots
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_acc, color='green', linestyle='-', 
        label='train accuracy'
    )
    plt.plot(
        valid_acc, color='blue', linestyle='-', 
        label='validataion accuracy'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig('output/accuracy.png')
    
    # loss plots
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_loss, color='orange', linestyle='-', 
        label='train loss'
    )
    plt.plot(
        valid_loss, color='red', linestyle='-', 
        label='validataion loss'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig('output/loss.png')
def calculateAUC (y_score,y_true,disease):
    y_score=torch.sigmoid(y_score)
    y_score=y_score.cpu().detach().numpy()
    y_true=y_true.cpu().detach().numpy()
    AUC=[]
    for i in range (y_score.shape[1]):
        y_t=y_true[:,i].copy()
        y_s=y_score[:,i].copy()
        if len(np.unique(y_t )) !=2:
            # print ("only one class present in disease "+str(i))
            continue         
        else:
            score =roc_auc_score(y_true=y_true[:,i].copy(),y_score=y_score[:,i].copy()) 
            score=round(score, 2)
            AUC.append ( ("class {}".format(disease[i]),score))      
    return AUC

class Metric():
    def __init__(self,classes):
        self.classes=classes

    def compute_metrics(self,outputs, targets, losses):
        # shape work on tensor
        n_classes = outputs.shape[1]
        fpr, tpr, aucs, precision, recall = {}, {}, {}, {}, {}
        for i, clas in enumerate(self.classes):
            fpr[clas], tpr[clas], _ = roc_curve(targets[:,i], outputs[:,i])
            aucs[clas] = auc(fpr[clas], tpr[clas])
            precision[clas], recall[clas], _ = precision_recall_curve(targets[:,i], outputs[:,i])
            fpr[clas], tpr[clas], precision[clas], recall[clas] = fpr[clas].tolist(), tpr[clas].tolist(), precision[clas].tolist(), recall[clas].tolist()

        metrics = {
                    "meanAUC": np.mean(list(aucs.values()))
                    'fpr': fpr,
                'tpr': tpr,
                'aucs': aucs,
                'precision': precision,
                'recall': recall,
                'loss':loss
                
                }

        return metrics
class AverageMeter():
    def __init__():
        self.reset()
        
    def reset(self):
        self.ls=[]
        self.mean=0
        self.cur=0
    def update (self, item):
        self.ls.append(item)
        self.mean= np.mean(ls)
        self.cur=item




