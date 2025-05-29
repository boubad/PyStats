"""module statindex"""

import numpy as np
from random import shuffle


class StatIndex(object):
    def is_valid_indexes(inds: np.ndarray) -> bool:
        if inds is None:
            return False
        if not isinstance(inds, np.ndarray):
            return False
        if (inds.ndim != 1) or inds.size == 0:
            return False
        n = inds.size
        temp = [False] * n
        for i in range(n):
            ii = int(inds[i])
            if ii < 0 or ii >= n or temp[ii]:
                return False
            temp[ii] = True
        for i in range(n):
            if not temp[i]:
                return False
        return True

    def __init__(
        self,
        the_size: int = None,
        crit: float = None,
        initialindex: np.ndarray = None,
        must_shuffle: bool = False,
    ) -> None:
        self._criteria = None
        self._indexes = None
        if crit is not None and crit > 0.0:
            self.criteria = crit
        if initialindex is not None:
            if StatIndex.is_valid_indexes(initialindex):
                self._indexes = initialindex
                return
        if the_size is not None and the_size > 0:
            self.resize(the_size, must_shuffle)

    def __str__(self) -> str:
        if self.valid:
            sret = '{"criteria":' + str(self.criteria) + ', "indexes":['
            n = self.size
            inds = self.indexes
            for i in range(n):
                if i > 0:
                    sret = sret + ", "
                sret = sret + str(inds[i])
            sret = sret + "]}"
        else:
            sret = "invalid statindex"
        return sret

    def __getitem__(self, i: int) -> int:
        if i < 0 or i >= self.size:
            raise ValueError("index out of range")
        return self._indexes[i]

    def __setitem__(self, i: int, val: int) -> None:
        n = self.size
        if i < 0 or i >= n or val < 0 or val >= n:
            raise ValueError("index/value out of range")
        self._indexes[i] = val

    def __add__(self, other: object) -> object:
        return self.add(other)

    def __len__(self) -> int:
        return self.size

    def __eq__(self, other: object) -> bool:
        return self.is_equal(other)

    def __le__(self, other: object) -> bool:
        return self.is_less_than(other) or self.is_equal(other)

    def __lt__(self, other: object) -> bool:
        return self.is_less_than(other)

    @property
    def valid(self) -> bool:
        if not hasattr(self, "_indexes"):
            return False
        return StatIndex.is_valid_indexes(self._indexes)

    @property
    def size(self) -> int:
        if self.valid:
            return self._indexes.size
        return 0

    @property
    def criteria(self) -> float:
        if hasattr(self, "_criteria") and (self._criteria is not None):
            return float(self._criteria)
        return 0.0

    @property
    def has_criteria(self) -> bool:
        return self.criteria is not None and self.criteria > 0.0

    @criteria.setter
    def criteria(self, val: float) -> None:
        if val > 0.0:
            self._criteria = val

    @property
    def indexes(self) -> np.ndarray | None:
        if self.valid:
            return self._indexes
        return None

    @indexes.setter
    def indexes(self, val: np.ndarray) -> None:
        if StatIndex.is_valid_indexes(val):
            self._indexes = val
            self._criteria = None

    def initialize_size(self, n: int, must_shuffle: bool = False) -> None:
        self.resize(n, must_shuffle)

    def initialize_index(self, crit: float, inds: np.ndarray) -> None:
        if not StatIndex.is_valid_indexes(inds):
            return
        self.criteria = crit
        self._indexes = inds

    def clone(self) -> object:
        p = StatIndex()
        if self.valid:
            p._criteria = self._criteria
            p._indexes = np.copy(self._indexes)
        return p

    def resize(self, n: int, must_shuffle: bool = False) -> None:
        if n > 0:
            self._criteria = None
            self._indexes = np.arange(n)
            if must_shuffle and n > 1:
                ll = self._indexes.tolist()
                shuffle(ll)
                self._indexes = np.array(ll)

    def get_index_at(self, index: int) -> int:
        if (index < 0) or (index >= self.size):
            raise ValueError("index out of range")
        return self._indexes[index]

    def shuffle(self) -> None:
        if self.valid and (self.size > 2):
            ll = self._indexes.tolist
            shuffle(ll)
            self._indexes = np.array(ll)

    def is_less_than(self, other: object) -> bool:
        if not self.has_criteria:
            return False
        if other is None:
            return True
        if not isinstance(other, StatIndex):
            return True
        if not other.has_criteria:
            return True
        return float(self.criteria) < float(other.criteria)

    def is_equal(self, other: object) -> bool:
        if other is None:
            return False
        if not isinstance(other, StatIndex):
            return False
        if not self.valid or not other.valid:
            return False
        if self.size != other.size:
            return False
        for i in range(self.size):
            if self.indexes[i] != other.indexes[i]:
                return False
        return True

    def is_reverse(self, other: object) -> bool:
        if other is None:
            return False
        if not isinstance(other, StatIndex):
            return False
        if not self.valid or not other.valid:
            return False
        n = self.size
        if other.size != n:
            return False
        i1 = 0
        i2 = n - 1
        while i1 < i2:
            if self.indexes[i1] != other.indexes[i2]:
                return False
            i1 += 1
            i2 -= 1
        return True

    def add(self, other: object) -> object:
        if (
            (other is not None)
            and isinstance(other, StatIndex)
            and other.is_less_than(self)
        ):
            self.indexes = other.indexes
            self.criteria = other.criteria
            return True
        return self
