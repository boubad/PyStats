"""module statdataset"""

import numpy as np
from scipy.stats import rankdata
from info import csvutils
from info.distancestore import DistanceStore
from info.distanceutils import DistanceUtils
from info.partitioner import Partitioner


class StatDataset(object):
    def __init__(self):
        self._varnames = None
        self._indnames = None
        self._weights = None
        self._data = None

    @property
    def valid(self) -> bool:
        if (
            not hasattr(self, "_data")
            or not hasattr(self, "_varnames")
            or not hasattr(self, "_indnames")
            or not hasattr(self, "_weights")
        ):
            return False
        if (
            self._data is None
            or self._varnames is None
            or self._indnames is None
            or self._weights is None
        ):
            return False
        if not isinstance(self._data, np.ndarray):
            return False
        if self._data.ndim != 2:
            return False
        s = self._data.shape
        nr = s[0]
        nc = s[1]
        if nr < 1 or nc < 1:
            return False
        if not isinstance(self._varnames, list):
            return False
        if not isinstance(self._indnames, list):
            return False
        if not isinstance(self._weights, np.ndarray):
            return False
        if self._weights.ndim != 1:
            return False
        if self._weights.size != nc:
            return False
        if self._varnames.__len__() != nc:
            return False
        if self._indnames.__len__() != nr:
            return False
        return True

    def __str__(self) -> str:
        sret = "StatDataset (" + str(self.rows) + "," + str(self.cols) + ")"
        return sret

    @property
    def data(self) -> np.ndarray | None:
        return self._data

    def clean(self):
        self._varnames = None
        self._indnames = None
        self._weights = None
        self._data = None

    @property
    def varnames(self) -> list[str] | None:
        return self._varnames

    @property
    def cols(self) -> int:
        if not self.valid:
            return 0
        return self.data.shape[1]

    @property
    def rows(self) -> int:
        if not self.valid:
            return 0
        return self.data.shape[0]

    @property
    def indnames(self) -> list[str] | None:
        return self._indnames

    @property
    def weights(self) -> np.ndarray | None:
        if self._weights is None:
            return None
        return self._weights

    @weights.setter
    def weights(self, v: np.ndarray):
        if v is None:
            return
        if not isinstance(v, np.ndarray):
            return
        if v.ndim != 1:
            return
        if v.size != self.cols:
            return
        somme = 0.0
        for i in range(self.cols):
            x = float(v[i])
            if x < 0.0:
                return
            somme += x
        if somme <= 0.0:
            return
        self._weights = v

    def get_indiv_at(self, index: int) -> np.ndarray | None:
        if (not self.valid) or index < 0 or index >= self.rows:
            return None
        return self.data[index, :]

    def get_variable_at(self, index: int) -> np.ndarray | None:
        if (not self.valid) or index < 0 or index >= self.cols:
            return None
        return self.data[:, index]

    def get_variable_name(self, ivar: int) -> str:
        if (not self.valid) or ivar < 0 or ivar >= self.cols:
            return ""
        return self.varnames[ivar]

    def get_indiv_name(self, irow: int) -> str:
        if (not self.valid) or irow < 0 or irow >= self.rows:
            return ""
        return self.indnames[irow]

    def read_csv(
        self, filename: str, hasnames: bool = True, robust: bool = False
    ) -> bool:
        vinds, vnames, vlistdata = csvutils.read_csv(filename, hasnames)
        ncols = len(vnames)
        if ncols > 0 and len(vlistdata) > 0:
            self.clean()
            self._varnames = vnames
            self._weights = np.ones(ncols, dtype=float)
            self._indnames = vinds
            self._data = np.array(vlistdata)
            self.__compute_weights()
            if robust:
                self.transform_ranks()
            return self.valid
        return False

    def transform_ranks(self):
        if self.valid:
            self._data = rankdata(self._data, axis=0)

    def partition(
        self,
        categs_count: int = 5,
        mode: str = "bertin",
        refermode: str = "mean",
    ):
        if not self.valid:
            raise ValueError("cannot categorize")
        nr = self.rows
        if nr < 2:
            raise ValueError("cannot categorize")
        nc = self.cols
        for i in range(nc):
            vv = self.get_variable_at(i)
            item = Partitioner(
                data=vv, categs_count=categs_count, mode=mode, refermode=refermode
            )
            cur = item.categs
            if len(cur) != nr:
                raise ValueError("cannot categorize")
            for j in range(nr):
                x = float(cur[j])
                self._data[j, i] = x

    def get_rows_distances(self, metric: str = "manhattan") -> DistanceStore:
        r = DistanceStore()
        if self.valid:
            the_data = DistanceUtils.compute_distance_array(
                self.data, metric, 0, self._weights
            )
            r.data = the_data
        return r

    def get_cols_distances(self, metric: str = "manhattan") -> DistanceStore:
        r = DistanceStore()
        if self.valid:
            the_data = DistanceUtils.compute_distance_array(self.data, metric, 1)
            r.data = the_data
        return r

    def export(self) -> tuple[list[str], dict]:
        names = []
        odict = {}
        if self.valid:
            nrows = self.rows
            for i in range(nrows):
                s = self.indnames[i]
                names.append(s)
            ncols = self.cols
            for i in range(ncols):
                skey = self.varnames[i]
                xdata = []
                for j in range(nrows):
                    x = float(self.data[j, i])
                    xdata.append(x)
                odict[skey] = xdata
        return names, odict

    def export_indexes(
        self, rowindexes: np.ndarray, colindexes: np.ndarray
    ) -> tuple[list[str], dict]:
        names = []
        odict = {}
        if self.valid:
            nrows = len(rowindexes)
            ncols = len(colindexes)
            if nrows == self.rows and ncols == self.cols:
                for i in range(nrows):
                    ii = int(rowindexes[i])
                    s = self.indnames[ii]
                    names.append(s)
                for i in range(ncols):
                    ii = int(colindexes[i])
                    skey = self.varnames[ii]
                    xdata = []
                    for j in range(nrows):
                        jj = int(rowindexes[j])
                        x = float(self.data[jj, ii])
                        xdata.append(x)
                    odict[skey] = xdata
        return names, odict

    def __compute_weights(self) -> None:
        nc = len(self._varnames)
        somme = 0.0
        wl = [0.0] * nc
        for i in range(nc):
            vx = self._data[:, i]
            dev = np.var(vx)
            if dev <= 0.0:
                return
            w = 1.0 / dev
            somme += w
            wl[i] = w
        if somme <= 0.0:
            return
        self._weights = np.array(wl / somme)
