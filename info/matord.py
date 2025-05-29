""" module matord """
import numpy as np
from info.matriceitemtype import MatriceItemType
from info.statdataset import StatDataset
from info.statindex import StatIndex
from info.arrangeitem import ArrangeItem


class MatOrd(object):
    """class MatOrd"""

    def __init__(self, filename: str = "", hasnames: bool = True) -> None:
        self._oset = StatDataset()
        self._rowindex = StatIndex()
        self._colindex = StatIndex()
        if filename != "":
            self.read_csv(filename, hasnames)

    def __str__(self) -> str:
        sret = "MatOrd (" + str(self.rows) + "," + str(self.cols) + ")"
        return sret

    @property
    def valid(self) -> bool:
        return self._oset.valid and self._colindex.valid and self._rowindex.valid

    @property
    def dataset(self) -> StatDataset:
        return self._oset

    @dataset.setter
    def dataset(self, oset: StatDataset) -> None:
        if oset is not None and isinstance(oset, StatDataset) and oset.valid:
            self._oset = oset
            self._colindex = StatIndex(oset.cols)
            self._rowindex = StatIndex(oset.rows)

    @property
    def colindex(self) -> StatIndex:
        return self._colindex

    @colindex.setter
    def colindex(self, p: StatIndex) -> None:
        if p is None:
            raise ValueError("invalid parameter")
        if not isinstance(p, StatIndex):
            raise ValueError("invalid parameter")
        if not p.valid:
            raise ValueError("invalid parameter")
        if p.size != self.cols:
            raise ValueError("invalid parameter")
        self._colindex = p

    @property
    def rowindex(self) -> StatIndex:
        return self._rowindex

    @rowindex.setter
    def rowindex(self, p: StatIndex) -> None:
        if p is None:
            raise ValueError("invalid parameter")
        if not isinstance(p, StatIndex):
            raise ValueError("invalid parameter")
        if not p.valid:
            raise ValueError("invalid parameter")
        if p.size != self.rows:
            raise ValueError("invalid parameter")
        self._rowindex = p

    @property
    def rows(self) -> int:
        return self._oset.rows

    @property
    def cols(self) -> int:
        return self._oset.cols

    @property
    def indnames(self) -> list[str]:
        vret = []
        if self.valid:
            n = self.rows
            names = self.dataset.indnames
            inds = self.rowindex
            for i in range(n):
                ii = int(inds[i])
                vret.append(names[ii])
        return vret

    @property
    def varnames(self) -> list[str]:
        vret = []
        if self.valid:
            n = self.cols
            names = self.dataset.varnames
            inds = self.colindex
            for i in range(n):
                ii = int(inds[i])
                vret.append(names[ii])
        return vret

    @property
    def data(self) -> np.ndarray | None:
        if self.valid:
            nrows = self.rows
            ncols = self.cols
            vret = np.zeros((nrows, ncols))
            src = self.dataset.data
            for i in range(nrows):  # pylint: disable=C0200
                ii = int(self.rowindex[i])
                for j in range(ncols):  # pylint: disable=C0200
                    jj = int(self.colindex[j])
                    vret[i, j] = src[ii, jj]
            return vret
        return None

    @property
    def weights(self) -> np.ndarray | None:
        if self.valid:
            src = self.dataset.weights
            if (src is not None) and src.size == self.cols:
                vret = np.ones(self.cols)
                for i in range(self.cols):  # pylint: disable=C0200
                    vret[i] = src[int(self.colindex[i])]
                return vret
        return None

    def get_variable_at(self, index: int) -> np.ndarray | None:
        ii = int(self.colindex[index])
        return self.dataset.get_variable_at(ii)

    def get_indiv_at(self, index: int) -> np.ndarray | None:
        ii = int(self.rowindex[index])
        return self.dataset.get_indiv_at(ii)

    def transform_ranks(self) -> None:
        if self.valid:
            self._oset.transform_ranks()
        return None

    def arrange(
        self,
        metric: str = "manhattan",
        mode: MatriceItemType = MatriceItemType.ROWCOL,
        method: str = "tsp",
    ) -> None:
        if self.valid:
            if mode == MatriceItemType.ROWCOL:
                self.__arrange_rows(metric, mode=method)
                self.__arrange_cols(metric, mode=method)
            elif mode == MatriceItemType.ROW:
                self.__arrange_rows(metric, mode=method)
            elif mode == MatriceItemType.COL:
                self.__arrange_cols(metric, mode=method)
            else:
                self.__arrange_rows(metric, mode=method)
                self.__arrange_cols(metric, mode=method)
        return None

    def export(self) -> tuple[list[str], dict]:
        rowinds = self.rowindex.indexes
        colinds = self.colindex.indexes
        return self.dataset.export_indexes(rowinds, colinds)

    def partition(
        self,
        categs_count: int = 5,
        mode: str = "bertin",
        refermode: str = "mean",
    ) -> None:
        self.dataset.partition(
            categs_count=categs_count, mode=mode, refermode=refermode
        )

    def read_csv(
        self, filename: str, hasnames: bool = True, robust: bool = False
    ) -> bool:
        tset = StatDataset()
        if not tset.read_csv(filename=filename, hasnames=hasnames, robust=robust):
            return False
        self.dataset = tset
        return self.valid

    def __arrange_rows(self, metric: str , mode: str = "tsp") -> None:
        ds = self.dataset.get_rows_distances(metric)
        item = ArrangeItem()
        item.initialize_store(ds)
        if mode == "tsp":
            item.tsp_arrange()
        else:
            item.arrange()
        self._rowindex.initialize_index(item.criteria, item.indexes)
        return None

    def __arrange_cols(self, metric: str , mode: str = "tsp") -> None:
        ds = self.dataset.get_cols_distances(metric)
        item = ArrangeItem()
        item.initialize_store(ds)
        if mode == "tsp":
            item.tsp_arrange()
        else:
            item.arrange()
        self._colindex.initialize_index(item.criteria, item.indexes)
        return None
