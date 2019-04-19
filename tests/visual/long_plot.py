from ilya_ezplot import Metric, ez_plot

import random


def plot_longs():
    for n in [500, 5000, 20000]:
        long_metric = Metric('x', 'y')
        for i in range(n):
            long_metric.add_record(random.random(), random.random())

        ez_plot(long_metric, 'temp', name=f'longer_metric_{n}')


from cProfile import Profile

p = Profile()
p.runcall(plot_longs)
p.print_stats('cumulative')