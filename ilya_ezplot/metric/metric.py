from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List, Any, Dict, SupportsFloat
import copy
import pickle
import os

from ilya_ezplot.metric.cached_parameters_mixin import CachedParamMixin
from ilya_ezplot.metric.interpolate import missing_value

default_folder = "_ez_metrics"


@dataclass(eq=False)
class Metric(CachedParamMixin):
    name: str = field(default='unknown')
    x_label: str = field(default='x')
    y_label: str = field(default='y')
    data: DefaultDict[float, List[float]] = field(default_factory=lambda: defaultdict(list))
    style_kwargs: Dict[str: Any] = field(default_factory=lambda: {})

    @property
    def samples(self):
        # assert len(set( len(x) for x in self.data.values() )) == 1
        if not self.data:
            return 0
        return len(next(iter(self.data.values())))

    def _sort(self):
        temp = self.data
        self.data = defaultdict(list)
        self.data.update({k: v for k, v in sorted(temp.items())})

    def add_record(self, x: SupportsFloat, y: SupportsFloat):
        self.data[x].append(y)
        self.dirty()

    def add_ys(self, x: SupportsFloat, ys: List[SupportsFloat]):
        self.data[x].extend(ys)
        self.dirty()

    def add_arrays(self, xs: List[SupportsFloat], ys: List[SupportsFloat], new_sample=False):
        """
        Add a list of measurements to the metric. xs and ys must be arrays of same length.

        :param new_sample: If the arrays are to be considered a separate experiment,
        or a part of current experiment.
        """
        assert len(xs) == len(ys)
        self.add_dict({x:y for x, y in zip(xs, ys)}, new_sample)

    def add_dict(self, dictionary: Dict[SupportsFloat, SupportsFloat], new_sample=False):
        """
        :param dictionary: the dictionary to add to the metric
        :param new_sample: If the arrays are to be considered a separate experiment,
        or a part of current experiment.
        """
        if new_sample and self.samples:
            new = Metric()
            for x, y in dictionary.items():
                new.add_record(x, y)
            new = self.__add__(new)
            self.data = new.data

        else:
            for x, y in dictionary.items():
                self.add_record(x, y)

    def save(self, folder=default_folder):
        os.makedirs(folder, exist_ok=True)

        with open(os.path.join(folder, f"{self.name}.ezm"), 'wb') as f:
            pickle.dump(self, file=f)

    @staticmethod
    def load_all(folder=default_folder) -> List[Metric]:
        if not os.path.isdir(folder):
            raise FileNotFoundError(folder)

        metrics = []
        for file in os.listdir(folder):
            if file[-4:] == ".ezm":
                with open(os.path.join(folder, file), 'rb') as f:
                    metrics.append(pickle.load(f))

        return metrics

    def _merge_equal(self, b: Metric) -> Metric:
        """ Modifies metric data a and b looking for keys not shared between the two,
         and inserting interpolated values"""

        all_keys = set(self.data.keys()) | set(b.data.keys())
        a, b = copy.deepcopy(self), copy.deepcopy(b)

        for md in [a, b]:
            missing = {}

            for k in all_keys:
                if k not in md.data:
                    missing[k] = [missing_value(md, k)]

            md.data.update(missing)

        result = Metric(a.name, a.x_label, a.y_label)
        result.data.update({k: v for k, v in sorted(a.data.items())})
        for k, v in b.data.items():
            result.add_ys(x=k, ys=v)

        return result

    def _merge_in(self, small_other: Metric) -> Metric:

        assert small_other.samples == 1

        result = Metric(self.name, self.x_label, self.y_label)
        result.data.update(self.data)

        for k in result.data.keys():
            result.add_record(x=k, y=missing_value(small_other, k))

        return result

    def __add__(self, other: Metric) -> Metric:
        if self.samples == 0:
            return other
        elif other.samples == 0:
            return self

        self._sort()
        other._sort()

        if self.samples == other.samples:
            return self._merge_equal(other)
        else:
            smaller = min([self, other], key=lambda x: x.samples)
            bigger = max([self, other], key=lambda x: x.samples)

            return bigger._merge_in(smaller)

    def __radd__(self, other):
        # support sum
        assert other == 0
        return self
