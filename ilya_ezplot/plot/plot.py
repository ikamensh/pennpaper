from __future__ import annotations

from ilya_ezplot._processing.running_avg import apply_running_average
import statistics
import numpy as np
from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ilya_ezplot.plot import Metric

import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib import pyplot as plt

import os


def maybe_make_dir(folder):
    os.makedirs(folder, exist_ok=True)


def ez_plot(metric: Metric, folder, name=None):

    metric.sort()

    maybe_make_dir(folder)
    plt.clf()

    avg = np.array([sum(l) / len(l) for l in metric.data.values()])
    stdev = []
    for l in metric.data.values():
        if len(l) > 1:
            stdev.append(statistics.stdev(l))
        else:
            stdev.append(0)
    stdev = np.array(stdev)

    plt.plot(metric.data.keys(), avg)
    plt.fill_between(metric.data.keys(), avg - stdev, avg + stdev, alpha=0.2)
    plt.xlabel(metric.x_label)
    plt.ylabel(metric.y_label)
    plt.grid()

    path = os.path.join(
        folder,
        (name or f"{metric.y_label}_{metric.x_label}") +
        ".png")
    print(path)
    plt.savefig(path)


def plot_group(metrics: Dict[str, Metric], folder: str, name: str = None):

    matplotlib.rcParams.update({'font.size': 3})

    maybe_make_dir(folder)
    plt.clf()

    metric = list(metrics.values())[0]
    plt.xlabel(metric.x_label)
    plt.ylabel(metric.y_label)
    plt.grid()

    for label, metric in metrics.items():

        avg = np.array([sum(l) / len(l) for l in metric.data.values()])
        stdev = []
        for l in metric.data.values():
            if len(l) > 1:
                stdev.append(statistics.stdev(l))
            else:
                stdev.append(0)
        stdev = np.array(stdev)

        smoothen = len(avg) / (len(avg) + 100)

        avg = apply_running_average(avg, smoothen)
        stdev = apply_running_average(stdev, smoothen) / 3

        style = {"linewidth":0.65}
        style.update(metric.style_kwargs)
        plt.plot(metric.data.keys(), avg, label=label, **style)
        maybe_color = {'color': style['color']} if 'color' in style else {}
        plt.fill_between(
            metric.data.keys(),
            avg - stdev,
            avg + stdev,
            alpha=0.2,
            **maybe_color
        )

    plt.legend(loc='best')
    path = os.path.join(
        folder,
        (name or f"{metric.y_label}_{metric.x_label}") +
        ".png")
    print(path)
    plt.savefig(path, dpi=300)



# def plot_many(name, folder, *args):
#     maybe_make_dir(folder)
#     plt.clf()
#     for array in args:
#         plt.plot(array)
#     plt.ylabel(name)
#     plt.xlabel('Generation')
#     plt.grid()
#     plt.savefig(os.path.join(folder, name + ".png"))


def plot_histogram(array, name, folder):
    maybe_make_dir(folder)
    plt.clf()
    plt.hist(array)
    plt.savefig(os.path.join(folder, name + ".png"))