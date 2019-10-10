import numpy as np


def conv_smooth(y, smoothen):
    box_pts = int(2 * smoothen * len(y) ** (2 / 3)) + 1

    box = np.hstack([np.arange(box_pts), np.flip(np.arange(box_pts))]) + 1
    box = box * (1 / np.sum(box))

    y_smooth = np.convolve(y, box, mode="same")

    repair = np.ones_like(y)
    repair = np.convolve(repair, box, mode="same")

    return y_smooth / repair
