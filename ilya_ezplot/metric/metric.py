from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, List, Any, Dict
import copy


from ilya_ezplot.metric.cached_parameters_mixin import CachedParamMixin
from ilya_ezplot.metric.interpolate import missing_value


@dataclass(eq=False)
class Metric(CachedParamMixin):
    x_label: str
    y_label: str
    data: DefaultDict[float, List[float]] = field(default_factory=lambda: defaultdict(list))
    style_kwargs: Dict[str: Any] = field(default_factory=lambda: {})


    @property
    def samples(self):
        # assert len(set( len(x) for x in self.data.values() )) == 1
        return len( next( iter(self.data.values()) ) )

    def sort(self):
        temp = self.data
        self.data = defaultdict(list)
        self.data.update( {k:v for k,v in sorted(temp.items())})

    def add_record(self, x: float, y: float):
        self.data[x].append(y)
        self.dirty()

    def add_many(self, x: float, ys: List[float]):
        self.data[x].extend(ys)
        self.dirty()



    def merge_equal(self, b: Metric) -> Metric:
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

        result = Metric(a.x_label, a.y_label)
        result.data.update({k: v for k, v in sorted(a.data.items())})
        for k, v in b.data.items():
            result.add_many(x=k, ys=v)

        return result


    def merge_in(self, small_other:Metric) -> Metric:

            assert small_other.samples == 1

            result = Metric(self.x_label, self.y_label)
            result.data.update(self.data)


            for k in result.data.keys():
                result.add_record(x=k, y=missing_value(small_other, k))

            return result


    def __add__(self, other: Metric) -> Metric:
        if self.samples == other.samples:
            return self.merge_equal(other)
        else:
            smaller = min([self, other], key=lambda x: x.samples)
            bigger = max([self, other], key=lambda x: x.samples)

            return bigger.merge_in(smaller)

    def __radd__(self, other):
        # support sum
        assert other == 0
        return self


