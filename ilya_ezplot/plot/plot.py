from __future__ import annotations

from ilya_ezplot.processing.running_avg import apply_running_average
from ilya_ezplot.processing.momentum import apply_momentum
import statistics
import numpy as np
from typing import Dict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ilya_ezplot import Metric

import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib import pyplot as plt

import os


def maybe_make_dir(folder):
    os.makedirs(folder, exist_ok=True)


def ez_plot(metric: Metric, folder, name=None):

    maybe_make_dir(folder)
    plt.clf()

    plt.xlabel(metric.x_label)
    plt.ylabel(metric.y_label)
    plt.grid()

    _plot(metric.y_label, metric)


    path = os.path.join(folder, (name or f"{metric.y_label}_{metric.x_label}") + ".png")
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
        _plot(label, metric, stdev_factor = 0.7)
    plt.legend(loc='best')

    path = os.path.join(folder, (name or f"{metric.y_label}_{metric.x_label}") + ".png")
    print(path)
    plt.savefig(path, dpi=275)


def _plot(label: str, metric: Metric, stdev_factor: float = 1.):
    """
    Add a curve to the plot, based on the given metric. Applies adaptive running average and
    plots the standard deviation as shaded area (scaled by stdev_factor).

    :param label: legend name for the curve
    """
    metric.sort()
    avg = np.array([sum(l) / len(l) for l in metric.data.values()])

    smoothen = 0.6 + 0.399 * len(avg) / (len(avg) + 100)
    avg = apply_running_average(avg, smoothen)
    style = {"linewidth": 0.8}
    style.update(metric.style_kwargs)
    plt.plot(metric.data.keys(), avg, label=label, **style)

    if metric.samples > 1:
        stdev = np.std(np.array( list(metric.data.values())), axis=1)
        stdev = apply_running_average(stdev, smoothen) * stdev_factor
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