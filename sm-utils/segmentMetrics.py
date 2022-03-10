import numpy as np

def pixel_acc(y_true: np.array, y_pred: np.array):
    """Calculate pixelwise accuracy between two images"""
    return (y_true == y_pred).mean()


def iou_coef(y_true: np.array, y_pred: np.array):
    """Calculate IoU (Intersection over Union) coefficient"""
    intersection = np.logical_and(y_true, y_pred)
    union = np.logical_or(y_true, y_pred)
    if union.sum() == 0:
        return 1
    iou = intersection.sum()/union.sum()
    return iou


def dice_coef(y_true: np.array, y_pred: np.array):
    """Calculate Dice coefficient"""
    intersection = np.logical_and(y_true, y_pred)
    if y_true.sum()+y_pred.sum() == 0:
        return 1
    dice = (2*intersection.sum())/(y_true.sum()+y_pred.sum())
    return dice