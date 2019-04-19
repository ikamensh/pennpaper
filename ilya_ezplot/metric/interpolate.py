from __future__ import annotations
from typing import DefaultDict, List, Tuple, TYPE_CHECKING
import bisect

if TYPE_CHECKING:
    from ilya_ezplot import Metric


metric_key = float
metric_data = DefaultDict[metric_key, List[float]]
def avg(a): return sum(a) / len(a)

def find_closest(m: Metric, key: metric_key) -> Tuple[metric_key, metric_key]:
    """ assumes keys are sorted."""
    if m.keysmin >= key: # neet to extrapolate
        left, right = m.all_keys[:2]
    elif m.keysmax <= key:
        left, right = m.all_keys[-2:]
    else:
        idx = bisect.bisect(m.all_keys, key)
        left, right = m.all_keys[idx-1], m.all_keys[idx]

    return left, right

def missing_value(m: Metric, key: metric_key) -> float:
    """ uses interpolation or extrapolation to insert an intermediate value into mapping """

    left, right = find_closest(m, key=key)
    val_left, val_right = avg(m.data[left]), avg(m.data[right])
    slope = (val_right - val_left) / (right - left)
    dx = key - left

    new_value = val_left + slope * dx
    new_value = min(new_value, m.valmax)
    new_value = max(new_value, m.valmin)
    return new_value




