from ilya_ezplot import Metric, plot_group

import math
import random

def many_plots():
    def one_series(shift):
        metrics = [Metric('x', 'y') for x in range(10)]
        for m in metrics:
            for i in range(40000):
                m.add_record(i, random.random() + shift + 0.4*math.sin(i/200))
            m._sort()


        return sum(metrics)

    many = {f"random line {i}":one_series(i) for i in range(5)}

    plot_group(many, 'temp', name="many_series")



from cProfile import Profile

p = Profile()
p.runcall(many_plots)
p.print_stats('cumulative')