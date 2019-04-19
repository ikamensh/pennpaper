from __future__ import annotations
from typing import DefaultDict, List
import itertools

class CachedParamMixin:
    data: DefaultDict[float, List[float]] = None

    def __init__(self):
        self._all_keys = None
        self._keysmax = None
        self._keysmin = None
        self._valmax = None
        self._valmin = None

    @property
    def all_keys(self):
        if self._all_keys is None:
            self._all_keys = list(self.data.keys())
        return self._all_keys

    @property
    def keysmax(self):
        if self._keysmax is None:
            self._keysmax = max(self.data.keys())
        return self._keysmax

    @property
    def keysmin(self):
        if self._keysmin is None:
            self._keysmin = min(self.data.keys())
        return self._keysmin

    @property
    def valmax(self):
        if self._valmax is None:
            self._valmax = max(itertools.chain.from_iterable(self.data.values()))
        return self._valmax

    @property
    def valmin(self):
        if self._valmin is None:
            self._valmin = min(itertools.chain.from_iterable(self.data.values()))
        return self._valmin

    def dirty(self):
        self._valmax = None
        self._valmin = None
        self._keysmax = None
        self._keysmin = None
        self._all_keys = None