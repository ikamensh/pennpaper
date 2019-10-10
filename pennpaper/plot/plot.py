from pennpaper.processing.conv import conv_smooth as smoothen_func
import numpy as np
from typing import List
from typing import TYPE_CHECKING
import warnings

if TYPE_CHECKING:
    from pennpaper import Metric

import matplotlib
from matplotlib import pyplot as plt

import os


def maybe_make_dir(folder):
    os.makedirs(folder, exist_ok=True)


def plot(
    metric: "Metric",
    folder: str = "_plots",
    name=None,
    smoothen=False,
    stdev_factor=None,
):

    if not metric.samples:
        warnings.warn(f"An empty metric {metric.name} can't be plotted!")
        return

    maybe_make_dir(folder)
    plt.clf()

    plt.xlabel(metric.x_label)
    plt.ylabel(metric.y_label)
    plt.grid()

    _plot(metric, smoothen, stdev_factor=stdev_factor)
    plt.legend(loc="best")

    filename = (name or metric.name) + ("_smooth" if smoothen else "") + ".png"
    files = list(os.listdir(folder))
    ctr = 0
    while filename in files:
        ctr += 1
        filename = (
            (name or metric.name) + f"_{ctr}" + ("_smooth" if smoothen else "") + ".png"
        )

    path = os.path.join(folder, filename)
    print(path)
    plt.savefig(path)


def plot_group(
    metrics: List["Metric"],
    folder: str = "_plots",
    name: str = None,
    smoothen=False,
    stdev_factor=None,
):

    matplotlib.rcParams.update({"font.size": 8})

    maybe_make_dir(folder)
    plt.clf()

    metric = metrics[0]
    plt.xlabel(metric.x_label)
    plt.ylabel(metric.y_label)
    plt.grid()

    any_plotted = False
    for metric in metrics:
        if not metric.samples:
            warnings.warn(f"An empty metric {metric.name} can't be plotted!")
            continue
        any_plotted = True
        _plot(metric, smoothen, stdev_factor=stdev_factor or 0.7)

    if not any_plotted:
        warnings.warn(f"All metrics were empty - no plot file will be generated.")
        return

    plt.legend(loc="best")

    filename = f"{name or metric.name}_group" + ("_smooth" if smoothen else "") + ".png"
    files = list(os.listdir(folder))
    ctr = 0
    while filename in files:
        ctr += 1
        filename = (
            f"{name or metric.name}_group"
            + f"_{ctr}"
            + ("_smooth" if smoothen else "")
            + ".png"
        )

    path = os.path.join(folder, filename)
    print(path)
    plt.savefig(path, dpi=275)


def _plot(metric: "Metric", smoothen: bool, stdev_factor: float, label: str = None):
    """
    Add a curve to the plot, based on the given metric. Applies adaptive running average and
    plots the standard deviation as shaded area (scaled by stdev_factor).

    :param label: legend name for the curve
    """

    smoothen_k = 0.25

    metric._sort()
    avg = np.array([sum(l) / len(l) for l in metric.data.values()])

    if smoothen:
        # smoothen_k = 0.1 + 0.899 * len(avg) / (len(avg) + 100)
        avg = smoothen_func(avg, smoothen_k)
    style = {"linewidth": 0.8}
    style.update(metric.style_kwargs)
    plt.plot(list(metric.data.keys()), avg, label=label or metric.name, **style)

    if metric.samples > 1:
        stdev = np.std(np.array(list(metric.data.values())), axis=1)
        if smoothen:
            stdev = smoothen_func(stdev, smoothen_k)
        if stdev_factor is not None:
            stdev *= stdev_factor
        stdev = np.array(stdev)

        maybe_color = {"color": style["color"]} if "color" in style else {}
        plt.fill_between(
            metric.data.keys(), avg - stdev, avg + stdev, alpha=0.2, **maybe_color
        )


def plot_histogram(array, name, folder):
    maybe_make_dir(folder)
    plt.clf()
    plt.hist(array)
    plt.savefig(os.path.join(folder, name + ".png"))
