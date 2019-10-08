import numpy as np

from pennpaper import Metric, plot_group


xs = np.arange(0.1, 5, step=0.01)

def noisy_mapping( mapping ):
    def _(x):
        y = mapping(x)
        y += np.random.normal(size=y.size)
        return y
    return _

funcs = {}
funcs['sin'] = noisy_mapping(np.sin)
funcs['log'] = noisy_mapping(np.log)
funcs['pow1.5'] = noisy_mapping(lambda x: x**(3/2))


from collections import defaultdict

metrics = defaultdict(list)

for i in range(30):
    for name, f in funcs.items():
        m = Metric(name)
        m.add_arrays(xs, f(xs))
        metrics[m.name].append(m)

metrics = [sum(v) for v in metrics.values()]

plot_group(metrics, name='smooth')
plot_group(metrics, name='true', smoothen=False)




