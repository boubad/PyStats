import numpy as np
from numpy import floating, median
from typing import Any


class VariableInfo(object):
    """class VariableInfo"""
    def __init__(self, data: np.ndarray[Any, Any], vname: str = "") -> None:
        self._name = ""
        self._min = None
        self._max = None
        self._mean = None
        self._median = None
        self._deviation = None
        self.set_data(data, vname)

    def __str__(self) -> str:
        sret = (
            '{"name":"'
            + self._name
            + '", "min":'
            + str(self._min)
            + ', "max":'
            + str(self._max)
            + ', "mean":'
            + str(self._mean)
            + ', "deviation":'
            + str(self._deviation)
            + "}"
        )
        return sret

    @property
    def name(self) -> str:
        return self._name

    @property
    def min(self) -> float | None:
        return self._min

    @property
    def max(self) -> float | None:
        return self._max

    @property
    def mean(self) -> float | None:
        return self._mean

    @property
    def median(self) -> floating[Any] | None:
        return self._median

    @property
    def deviation(self) -> float | None:
        return self._deviation

    @property
    def valid(self) -> bool:
        if self._min is None or self._max is None or self._min >= self._max:
            return False
        if self._mean is None or self._mean < self._min or self._mean > self._max:
            return False
        if self._median is None or self._median < self._min or self._median > self._max:
            return False
        if self._deviation is None or self._deviation <= 0.0:
            return False
        return True
    def set_data(self, data: np.ndarray[Any, Any], vname: str = "") -> None:
        self._name = vname
        self._min = None
        self._max = None
        self._mean = None
        self._deviation = None
        self._median = None
        if data.ndim != 1:
            return
        n = data.size
        if n > 0:
            self._min = data.min()
            self._max = data.max()
            self._mean = data.mean()
            self._median = median(data)
            self._deviation = data.std()
