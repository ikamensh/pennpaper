import numpy as np

from ilya_ezplot import Metric, plot_group

xs = np.arange(0.1, 5, step=0.01)

funcs = {}
funcs['sin'] = np.sin
funcs['log'] = np.log
funcs['pow1.5'] = lambda x: x**(3/2)

metrics = {}

for name, f in funcs.items():
    m = Metric('x', 'y')
    m.add_arrays(xs, f(xs))
    metrics[name] = m

plot_group(metrics)
plot_group(metrics, name='true', smoothen=False)




