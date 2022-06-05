import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Sequence


def plot_confusion_matrix(
    y_true: Sequence,
    y_pred: Sequence,
    y_pred_scores: Sequence = None,
    labels: Sequence = None
):
    """Creates confusion matrix with confidence scores.

    Parameters:
    -----------
    y_true: Sequence
        true/actual labels
    y_pred: Sequence
        predicted labels
    y_pred_scores: Sequence
        predicted label confidence score
    labels: Sequence
        label names in order to be displayed
    """
    if not labels:
        labels = np.unique(list(y_true)+list(y_pred))

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    if y_pred_scores is not None:
        y_pred_scores = np.array(y_pred_scores)

    cm = np.zeros((len(labels), len(labels))) #Count matrix
    if y_pred_scores is not None:
        cs = np.zeros((len(labels), len(labels))) #Confidence score matrix

    #Fill count and mean scores
    for a, l in enumerate(labels):
        for p, ol in enumerate(labels):
            cm[a][p] = (y_pred[y_true==l]==ol).sum()
            if y_pred_scores is not None:
                scores = y_pred_scores[y_true==l][y_pred[y_true==l]==ol]
                cs[a][p] = 0 if len(scores) == 0 else scores.mean()

    cn = cm / cm.sum(axis=0, keepdims=True) #Normalised matrix for cell color

    # Annotation labels
    if y_pred_scores is not None:
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
    else:
        annot_matrix = [
            [
                '{}\n({})'.format(
                    int(cm[i][j])
                )
                for j in range(len(labels))
            ]
            for i in range(len(labels))
        ]

    # Plot Matrix
    fig, axes = plt.subplots(1,1, figsize=(len(labels) + 5, len(labels) + 2))
    sns.heatmap(cn, annot=annot_matrix, fmt='', cmap='viridis', ax=axes)
    axes.set_title('Confusion Matrix (with count, confidence)')
    axes.set_xticklabels(labels)
    axes.set_xlabel("Predicted")
    axes.set_yticklabels(labels)
    axes.set_ylabel("Actual")
    axes.xaxis.tick_top()
    fig.show()
