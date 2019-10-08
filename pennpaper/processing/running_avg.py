from typing import List
import numpy as np


def _running_avg(data: List[float], smoothen: float = 0.1):
    if len(data) == 0:
        return data

    result = [data[0]]
    for x in data[1:]:
        result.append(result[-1] * smoothen + x * (1 - smoothen))
    result = np.array(result)
    return result

def apply_running_average(data: List[float], smoothen: float = 0.1):
    assert 0 < smoothen < 1

    forward = _running_avg(data, smoothen)

    data_backward = list(reversed(data))
    backward = _running_avg(data_backward, smoothen)
    backward = np.array(list(reversed(backward)))

    return (forward + backward) / 2



