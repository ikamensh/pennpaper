import numpy as np

from pennpaper import Metric, plot_group

xs = np.arange(0.1, 5, step=0.01)

uni_noise = lambda x: np.random.uniform(size=x.shape) + x

funcs = {}
funcs['uniform'] = lambda x: np.random.uniform(size=x.shape) + x
funcs['weibull'] = lambda x: np.random.weibull(a=1, size=x.shape) + x
funcs['beta'] = lambda x: np.random.beta(a=1, b=1, size=x.shape) + x

metrics = []

for name, f in funcs.items():
    m = Metric(name=name)
    for i in range(100):
        m.add_arrays(uni_noise(xs), f(xs), new_sample=True)

    metrics.append(m)

plot_group(metrics)
plot_group(metrics, name='true', smoothen=False)