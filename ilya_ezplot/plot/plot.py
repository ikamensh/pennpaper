from __future__ import annotations

from ilya_ezplot.processing.running_avg import apply_running_average
import numpy as np
from typing import List
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ilya_ezplot import Metric

import matplotlib
from matplotlib import pyplot as plt

import os


def maybe_make_dir(folder):
    os.makedirs(folder, exist_ok=True)


def ez_plot(metric: Metric, folder: str = '_plots', name=None, smoothen = True):

    maybe_make_dir(folder)
    plt.clf()

    plt.xlabel(metric.x_label)
    plt.ylabel(metric.y_label)
    plt.grid()

    _plot(metric, smoothen)
    plt.legend(loc='best')

    path = os.path.join(folder, (name or metric.name) + ".png")
    print(path)
    plt.savefig(path)


def plot_group(metrics: List[Metric], folder: str = '_plots', name: str = None, smoothen = True):

    matplotlib.rcParams.update({'font.size': 8})

    maybe_make_dir(folder)
    plt.clf()

    metric = metrics[0]
    plt.xlabel(metric.x_label)
    plt.ylabel(metric.y_label)
    plt.grid()

    for metric in metrics:
        _plot(metric, smoothen, stdev_factor = 0.7)
    plt.legend(loc='best')

    path = os.path.join(folder, (name or f"{metric.y_label}_{metric.x_label}") + ".png")
    print(path)
    plt.savefig(path, dpi=275)


def _plot(metric: Metric, smoothen: bool, stdev_factor: float = 1., label:str = None):
    """
    Add a curve to the plot, based on the given metric. Applies adaptive running average and
    plots the standard deviation as shaded area (scaled by stdev_factor).

    :param label: legend name for the curve
    """
    metric._sort()
    avg = np.array([sum(l) / len(l) for l in metric.data.values()])

    if smoothen:
        smoothen_k = 0.1 + 0.899 * len(avg) / (len(avg) + 100)
        avg = apply_running_average(avg, smoothen_k)
    style = {"linewidth": 0.8}
    style.update(metric.style_kwargs)
    plt.plot(list(metric.data.keys()), avg, label=label or metric.name, **style)

    if metric.samples > 1:
        stdev = np.std(np.array( list(metric.data.values())), axis=1)
        if smoothen:
            stdev = apply_running_average(stdev, smoothen_k) * stdev_factor
        stdev = np.array(stdev)

        maybe_color = {'color': style['color']} if 'color' in style else {}
        plt.fill_between(
            metric.data.keys(),
            avg - stdev,
            avg + stdev,
            alpha=0.2,
            **maybe_color
        )


def plot_histogram(array, name, folder):
    maybe_make_dir(folder)
    plt.clf()
    plt.hist(array)
    plt.savefig(os.path.join(folder, name + ".png"))