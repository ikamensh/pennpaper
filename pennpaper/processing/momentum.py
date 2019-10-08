from typing import List
import numpy as np

def _momentum(data: List[float], smoothen: float = 0.1):

    result = [data[0]]
    dx = 0

    for i, x in enumerate(data[1:], start=1):
        dx = dx * smoothen + (1-smoothen) * (x - data[i-1])
        result.append(result[-1] + dx)

    result = np.array(result)

    return result

def apply_momentum(data: List[float], smoothen: float = 0.1):
    assert 0 < smoothen < 1

    forward = _momentum(data, smoothen)

    data_backward = list(reversed(data))
    backward = _momentum(data_backward)
    backward = np.array(list(reversed(backward)))

    return (forward + backward) / 2







