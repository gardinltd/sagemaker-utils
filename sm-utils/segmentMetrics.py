import numpy as np

def get_dice_coef(y_true: np.array, y_pred: np.array):
    """Calculate Dice coefficient"""
    intersection = np.logical_and(y_true, y_pred)
    if y_true.sum()+y_pred.sum() == 0:
        return 1
    return (2*intersection.sum())/(y_true.sum()+y_pred.sum())

def get_pixel_acc(y_true: np.array, y_pred: np.array):
    """Calculate pixelwise accuracy between two images"""
    return (y_true == y_pred).mean()

def get_iou_coef(y_true: np.array, y_pred: np.array):
    """Calculate IoU (Intersection over Union) coefficient"""
    intersection = np.logical_and(y_true, y_pred)
    union = np.logical_or(y_true, y_pred)
    if union.sum() == 0:
        return 1
    return intersection.sum()/union.sum()

def get_multiclass_iou(y_true: np.array, y_pred: np.array):
    classes = set(np.unique(y_true))
    classes.update(np.unique(y_pred))
    ious = [get_iou_coef((y_true==c).astype('uint8'), (y_pred==c).astype('uint8')) for c in list(classes)]
    return np.mean(ious)

def get_multiclass_dice(y_true: np.array, y_pred: np.array):
    classes = set(np.unique(y_true))
    classes.update(np.unique(y_pred))
    dices = [get_dice_coef((y_true==c).astype('uint8'), (y_pred==c).astype('uint8')) for c in list(classes)]
    return np.mean(dices)
