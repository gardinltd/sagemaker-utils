import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Sequence

def plot_confusion_matrix(
    y_true: Sequence, 
    y_pred: Sequence, 
    y_pred_scores: Sequence, 
    labels: Sequence = None
):
    if not labels:
        labels = np.unique(y_true)
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_pred_scores = np.array(y_pred_scores)
        
    cm = np.zeros((len(labels), len(labels)))
    cs = np.zeros((len(labels), len(labels)))
    for a, l in enumerate(labels):
        for p, ol in enumerate(labels):
            cm[a][p] = (y_pred[y_true==l]==ol).sum()
            scores = y_pred_scores[y_true==l][y_pred[y_true==l]==ol]
            if len(scores) == 0:
                cs[a][p] = 0
            else:
                cs[a][p] = scores.mean()
    
    cn = cm / cm.sum(axis=0, keepdims=True)
    
    annot_matrix = [
        [
            '{}\n({})'.format(
                int(cm[i][j]), 
                round(cs[i][j], 2)
            ) 
            for j in range(len(labels))
        ] 
        for i in range(len(labels))
    ]
    
    fig, axes = plt.subplots(1,1, figsize=(len(labels) + 5, len(labels) + 2))
    sns.heatmap(cn, annot=annot_matrix, fmt='', cmap='viridis', ax=axes)
    axes.set_title('Confusion Matrix (with count, confidence)')
    axes.set_xticklabels(labels)
    axes.set_yticklabels(labels)
    fig.show()
