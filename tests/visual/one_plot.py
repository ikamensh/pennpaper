from ilya_ezplot import Metric, ez_plot

import random

metrics = [Metric('x', 'y') for x in range(10)]
for m in metrics:
    for i in range(50):
        m.add_record(random.random(), random.random())
    m._sort()


m11 = sum(metrics)

ez_plot(metrics[0], 'temp', name="single_random")
ez_plot(m11, 'temp', name="summ_10_random")

straight = Metric('x', 'y')
for i in range(50):
    straight.add_record(i, i + 0.1*random.random())

ez_plot(straight, 'temp', name='straight')

