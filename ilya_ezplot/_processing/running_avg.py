from typing import List
import numpy as np


def apply_running_average(data: List[float], smoothen: float = 0.1):

    forward = [data[0]]

    for x in data[1:]:
        forward.append(forward[-1] * smoothen + x * (1 - smoothen))

    forward = np.array(forward)

    data_backward = list(reversed(data))

    backward = [data_backward[0]]

    for x in data_backward[1:]:
        backward.append(backward[-1] * smoothen + x * (1 - smoothen))

    backward = np.array(list(reversed(backward)))

    return (forward + backward) / 2


if __name__ == "__main__":
    x = list(range(10))

    print(x)
    print(apply_running_average(x))
    print(apply_running_average(x, 0.3))
    print(apply_running_average(x, 0.8))
