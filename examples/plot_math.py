import numpy as np
from matplotlib import pyplot as plt


def measure():
    def noisy_mapping( mapping ):
        def _(x):
            y = mapping(x)
            y += np.random.normal(0, 2, size=y.size)
            return y
        return _

    funcs = {}
    funcs['sin'] = noisy_mapping(np.sin)
    funcs['log'] = noisy_mapping(np.log)
    funcs['pow1.5'] = noisy_mapping(lambda x: x**(3/2))

    X = np.arange(0.1, 10, step=0.001)


    import pennpaper as pp
    from collections import defaultdict

    metrics = defaultdict(list)

    for i in range(90):
        for name, f in funcs.items():
            m = pp.Metric(name)
            m.add_arrays(X, f(X))
            metrics[m.name].append(m)

    metrics = [sum(v) for v in metrics.values()]

    pp.plot_group(metrics)
    pp.plot_group(metrics, smoothen=True)
    
from cProfile import Profile
p = Profile()
p.runcall(measure)
p.print_stats('cumulative')




