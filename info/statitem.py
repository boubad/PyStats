"""module statitem"""

import numpy as np
from info import distanceutils
from info.statitemstatustype import StatItemStatusType


class StatItem(object):
    """StatItem class definition"""

    def __init__(self, the_index: int = 0, the_id: str = "", the_size: int = 0) -> None:
        self._index = the_index
        self._name = the_id
        self._data = None
        self._status = StatItemStatusType.ACTIVE
        if the_size > 0:
            self._data = np.zeros(the_size, dtype=float)

    def __str__(self) -> str:
        sret = (
            '{"index":' + str(self._index) + ', "name": "' + self._name + '", "data": ['
        )
        n = self._data.size
        for i in range(n):
            if i > 0:
                sret = sret + ", "
            sret = sret + str(self._data[i])
        sret = sret + "]}"
        return sret

    @property
    def status(self) -> StatItemStatusType:
        return self._status

    @status.setter
    def status(self, s: StatItemStatusType) -> None:
        self._status = s

    def resize(self, n: int) -> None:
        if n >= 0:
            if n == 0:
                self._data = None
            else:
                if self._data is not None and self._data.size != n:
                    self._data = np.zeros(n, dtype=float)
                elif self._data is None:
                    # if data is None, we create a new array
                    self._data = np.zeros(n, dtype=float)

    def clone(self) -> object:
        p = StatItem()
        if self.valid:
            p._index = self._index
            p._name = self._name
            p._data = np.copy(self._data)
        return p

    @property
    def valid(self) -> bool:
        return (self._data is not None) and self._data.size > 0

    @property
    def size(self) -> int:
        if self._data is None:
            return 0
        return self._data.size

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, the_index: int) -> None:
        self._index = the_index

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, the_id: str) -> None:
        self._name = the_id

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, the_data: np.ndarray) -> None:
        if the_data is None:
            self._data = None
            return
        if not isinstance(the_data, np.ndarray):
            raise ValueError("invalid input type")
        if the_data.ndim != 1:
            raise ValueError("invalid input dimension")
        self._data = the_data

    def get_data_at(self, index: int) -> float:
        if not self.valid:
            raise ValueError("invalid statitem")
        if index < 0 or index >= self._data.size:
            raise ValueError("index out of range")
        return float(self._data[index])

    def set_data_at(self, index: int, val: float) -> None:
        if not self.valid:
            raise ValueError("invalid statitem")
        if index < 0 or index >= self._data.size:
            raise ValueError("index out of range")
        self._data[index] = float(val)

    def distance(
        self, other: object, metric: str = "euclidian", w: np.ndarray = None
    ) -> float:
        if other is None:
            raise ValueError("invalid parameter")
        if not isinstance(other, StatItem):
            raise ValueError("invalid parameter")
        n = self.size
        if n != other.size:
            raise ValueError("size mismatch")
        return distanceutils.DistanceUtils.distance(self.data, other.data, metric, w)
