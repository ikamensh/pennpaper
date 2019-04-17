from typing import DefaultDict, List, Tuple
import bisect


metric_key = float
metric_data = DefaultDict[metric_key, List[float]]
def avg(a): return sum(a) / len(a)

def find_closest(series: metric_data, key: metric_key) -> Tuple[metric_key, metric_key]:
    """ assumes keys are sorted."""
    keys = list(series.keys())
    if min(keys) >= key: # neet to extrapolate
        left, right = keys[:2]
    elif max(keys) <= key:
        left, right = keys[-2:]
    else:
        idx = bisect.bisect(keys, key)
        left, right = keys[idx-1], keys[idx]

    return left, right



def missing_value(series: metric_data, key: metric_key) -> float:
    """ uses interpolation or extrapolation to insert an intermediate value into mapping """

    left, right = find_closest(series, key)
    val_left, val_right = avg(series[left]), avg(series[right])
    slope = (val_right - val_left) / (right - left)
    dx = key - left

    new_value = val_left + slope * dx
    return new_value




