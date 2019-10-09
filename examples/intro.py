"""
We have a mysterious function that we would like to better understand on the interval [0.1, 5.].
Unfortunately the function is noisy.
"""
import numpy as np

X = np.arange(0.1, 5, step=0.01)

import random


def noisy_mapping(mapping):
    def _(x):
        y = mapping(x)
        y += random.gauss(0, 1)
        return y

    return _


pow2 = noisy_mapping(lambda x: x ** 2)


"""
lets record the pairs (x, f(x)) in a metric and make a plot:
"""

from pennpaper import Metric, plot_group, plot

m1 = Metric("pow2")
for x in X:
    m1.add_record(x, pow2(x))

plot(m1)


m2 = Metric("pow2_second_try")
for x in X:
    m2.add_record(x, pow2(x))

plot_group([m1, m2])


# Actually, m1 and m2 are metrics of the same process.
# What if we create a new metric tracking the mean and stddev of this process?
m3 = m1 + m2
plot(m3)

# the plot is too noisy to understand. We can smoothen it!
plot(m3, smoothen=True)
