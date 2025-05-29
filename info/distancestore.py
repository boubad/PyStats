"""module distancestore"""

import numpy as np


class DistanceStore(object):
    """class DistanceStore"""

    def __init__(self, n: int = 0) -> None:
        if n >= 0:
            self._data = np.zeros((n, n), dtype=float)
        else:
            self._data = np.zeros((0, 0), dtype=float)

    def __str__(self) -> str:
        sret = "DistanceStore size: " + str(self.size)
        return sret

    @property
    def valid(self) -> bool:
        if not hasattr(self, "_data"):
            return False
        if self._data is None:
            return False
        if not isinstance(self._data, np.ndarray):
            return False
        if self._data.ndim != 2:
            return False
        s = self._data.shape
        n = s[0]
        return (n > 0) and (s[1] == n) and (self._data.size == (n * n))

    def initialize_test(self, n: int) -> bool:
        self._data = np.zeros((n, n), dtype=float)
        for i in range(n):
            for j in range(i):
                if i > j:
                    fval = i - j
                    self._data[i, j] = fval
                    self._data[j, i] = fval
        return True

    @property
    def size(self) -> int:
        if self.valid:
            return self._data.shape[0]
        return 0

    @property
    def data(self) -> np.ndarray | None:
        if not self.valid:
            return None
        return self._data

    @data.setter
    def data(self, the_data: np.ndarray):
        if (
            (the_data is not None)
            and isinstance(the_data, np.ndarray)
            and the_data.ndim == 2
            and the_data.shape[1] == the_data.shape[0]
        ):
            self._data = the_data
        else:
            raise ValueError("Invalid data for DistanceStore")

    def get_at(self, first: int, second: int) -> float:
        n = self.size
        if (first < 0) or (first >= n) or (second < 0) or (second >= n):
            return 0.0
        return float(self.data[first, second])

    def set_at(self, first: int, second: int, val: float) -> None:
        n = self.size
        if (val < 0.0) or (first < 0) or (first >= n) or (second < 0) or (second >= n):
            return
        self.data[first, second] = val
