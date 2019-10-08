from pennpaper import Metric, plot

import random

metrics = [Metric('x', 'y') for x in range(10)]
for m in metrics:
    for i in range(50):
        m.add_record(random.random(), random.random())
    m._sort()


m11 = sum(metrics)

plot(metrics[0], 'temp', name="single_random")
plot(m11, 'temp', name="summ_10_random")

straight = Metric('x', 'y')
for i in range(50):
    straight.add_record(i, i + 0.1*random.random())

plot(straight, 'temp', name='straight')

