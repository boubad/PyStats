import numpy as np
import info.datautils as datautils


class Partitioner(object):
    def partition(
        data: np.ndarray,
        categs_count: int = 5,
        mode: str = "bertin",
        refermode: str = "mean",
    ) -> np.ndarray:
        if data is None or not isinstance(data, np.ndarray):
            raise ValueError("invalid input parameter")
        if data.ndim == 1:
            p = Partitioner(data, categs_count, mode, refermode)
            return np.array(p.categs)
        elif data.ndim == 2:
            nr = data.shape[0]
            nc = data.shape[1]
            vret = np.zeros((nr, nc), dtype=np.int32)
            for i in range(nc):
                p = Partitioner(data[:, i], categs_count, mode, refermode)
                src = p.categs
                for j in range(nr):
                    vret[j, i] = src[j]
            return vret
        return None

    def __init__(
        self,
        data: np.ndarray = None,
        categs_count: int = 5,
        mode: str = "bertin",
        refermode: str = "mean",
    ):
        if data is not None:
            if data.ndim != 1:
                raise ValueError("invalid input dimension")
        self._nbclasses = categs_count
        self._mode = mode
        self._refmode = refermode
        self._data = data
        self._limits = []
        self._results = []
        self.__update_item()

    def __str__(self) -> str:
        sret = (
            '{"categs_count":'
            + str(self._nbclasses)
            + ', "mode":'
            + '"'
            + self._mode
            + '"'
            + ',"refermode":'
            + '"'
            + self._refmode
            + '"'
            + ', "limits":['
        )
        for i in range(len(self._limits)):
            if i != 0:
                sret = sret + ", "
            sret = sret + str(self._limits[i])
        sret = sret + '],\n "categs":['
        for i in range(len(self._results)):
            if i != 0:
                sret = sret + ", "
            sret = sret + str(self._results[i])
        sret = sret + "]\n}"
        return sret

    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def mode(self, s: str):
        if (s != self._mode) and (s == "bertin" or s == "uniform"):
            self._mode = s
            self._limits = []
            self._results = []
            self.__update_item()

    @property
    def refmode(self) -> str:
        return self._refmode

    @refmode.setter
    def refmode(self, s: str):
        if (
            (s != self._refmode)
            and (self._mode == "bertin")
            and (s == "mean" or s == "median")
        ):
            self._refmode = s
            self._limits = []
            self._results = []
            self.__update_item()

    @property
    def categs_count(self) -> int:
        return self._nbclasses

    @categs_count.setter
    def categs_count(self, n: int) -> None:
        if n > 0:
            nx = n
            if self.mode == "bertin":
                if (nx % 2) == 0:
                    nx += 1
            self._nbclasses = nx
            self._limits = []
            self._results = []
            self.__update_item()
        return

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, d: np.ndarray):
        if d is not None and d.ndim != 1:
            raise ValueError("invalid input dimension")
        self._data = d
        self._limits = []
        self._results = []
        self.__update_item()

    @property
    def limits(self) -> list[float]:
        return self._limits

    @property
    def categs(self) -> list[int]:
        return self._results

    def __update_item(self) -> None:
        if (len(self._data) < 1) or (len(self._results) > 0):
            return
        if len(self._limits) < 1:
            if self._mode == "bertin":
                self.__init_bertin(self._refmode)
            else:
                self.__init_uniform()
            self.__recode_data()
        return None

    def __recode_data(self) -> None:
        d = self._data
        llx = self._limits
        m = len(llx)
        mm1 = m - 1
        dd = []
        for i in range(mm1):
            dd.append((llx[i], llx[i + 1]))
        nx = len(dd)
        n = len(d)
        self._results = [int(0)] * n
        for i in range(n):
            x = d[i]
            done = False
            for j in range(nx):
                if not done:
                    t = dd[j]
                    if (x >= t[0]) and (x <= t[1]):
                        self._results[i] = j
                        done = True
            if not done:
                self._results[i] = self._nbclasses - 1
        return None

    def __init_bertin(self, refmode: str = "mean") -> None:
        self._limits = []
        self._results = []
        d = self._data
        if len(d) < 1:
            return
        vmin = min(d)
        vmax = max(d)
        if vmin >= vmax:
            return
        bmedia = refmode == "median"
        self._results, self._limits = datautils.compute_bertin_classes(
            d, self._nbclasses, bmedia
        )

    def __init_uniform(self) -> None:
        self._limits = []
        self._results = []
        d = self._data
        if len(d) < 1:
            return
        vmin = min(d)
        vmax = max(d)
        if vmin >= vmax:
            return
        nb = self._nbclasses
        delta = (vmax - vmin) / nb
        x = vmin
        self._limits = [vmin]
        for i in range(nb):
            x += delta
            if x > vmax:
                x = vmax
            self._limits.append(x)
