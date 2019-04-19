from ilya_ezplot.processing.running_avg import apply_running_average
from ilya_ezplot.processing.momentum import apply_momentum

import random
for k_smoothen, tag in zip([0.3, 0.7, 0.95], [30, 70, 95]):

    x = [random.random() for i in range(100)]
    m = apply_momentum(x, smoothen=k_smoothen)
    s = apply_running_average(x, smoothen=k_smoothen)

    from ilya_ezplot.plot.plot import plt

    plt.clf()
    plt.plot(x, color = 'blue')
    plt.plot(s, color = 'green')
    plt.plot(m, color = 'red')
    plt.savefig(f'temp/noise{tag}.png')

    import math

    x = [0.001*i for i in range(10000)]
    y = [math.sin(e) + random.random() for e in x]
    my = apply_momentum(y, smoothen=k_smoothen)
    sy = apply_running_average(y, smoothen=k_smoothen)

    plt.clf()
    # plt.plot(y, color = 'blue')
    plt.plot(my, color = 'red')
    plt.plot(sy, color = 'green')
    plt.savefig(f'temp/sin{tag}.png')
