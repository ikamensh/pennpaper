import numpy as np

from pennpaper import Metric, plot_group, plot

def noisy_mapping( mapping ):
    def _(x):
        y = mapping(x)
        y += np.random.normal(size=y.size)
        return y
    return _

pow2 = noisy_mapping(lambda x: x**2)


X = np.arange(0.1, 5, step=0.01)
Y = pow2(X)

m = Metric('pow2')
m.add_arrays(X, Y)

plot(m, name='my_plot')


Y2 = pow2(X)

m2 = Metric('pow2_second_try')
m2.add_arrays(X, Y2)

plot_group([m, m2], name='my_plot_a_few')


plot(m + m2, name='my_plot')






