import numpy as np
from random import randrange
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_local_search, solve_tsp_simulated_annealing
from info.distancestore import DistanceStore
from info.statindex import StatIndex


class ArrangeItem(StatIndex):
    def __init__(self, the_size: int = 0, must_shuffle: bool = False) -> None:
        StatIndex.__init__(self, the_size, must_shuffle)
        self._store = DistanceStore()

    def initialize_store(self, st: DistanceStore, must_shuffle: bool = False) -> bool:
        if (st is not None) and isinstance(st, DistanceStore) and st.valid:
            self._store = st
            self.initialize_size(st.size, must_shuffle)
            self.compute_criteria()
            return True
        return False

    def initialize_test(self, n: int) -> bool:
        st = DistanceStore()
        if not st.initialize_test(n):
            return False
        return self.initialize_store(st, True)

    @property
    def store(self) -> DistanceStore:
        return self._store

    @store.setter
    def store(self, st: DistanceStore) -> None:
        self.initialize_store(st)

    def arrange(self) -> list[StatIndex]:
        lret = []
        if not self.valid:
            return lret
        best = StatIndex()
        pairs = self.__compute_best_starts()
        for pair in pairs:
            cur = self.__arrange_step(pair[0], pair[1])
            if cur.valid:
                if cur < best:
                    best = cur
                    lret = [
                        cur,
                    ]
                elif cur.criteria == best.criteria:
                    found = False
                    for x in lret:
                        if cur == x or cur.is_reverse(x):
                            found = True
                            break
                    if not found:
                        lret.append(cur)
        if best.valid:
            self.indexes = best.indexes
            self.criteria = best.criteria
        return lret

    def tsp_arrange(self) -> list[StatIndex]:
        lret = []
        if self.valid:
            distance_matrix = np.copy(self.store.data)
            distance_matrix[:, 0] = 0
            if self.size < 15:
                permutation2, distance2 = solve_tsp_dynamic_programming(distance_matrix)
            else:
                permutation = solve_tsp_simulated_annealing(distance_matrix)[0]
                permutation2, distance2 = solve_tsp_local_search(
                    distance_matrix, x0=permutation, perturbation_scheme="ps3"
                )
            self.indexes = np.array(permutation2)
            self.criteria = distance2
            item = StatIndex()
            item.initialize_index(self.criteria, self.indexes)
            lret.append(item)
        return lret

    def compute_criteria(self, curindexes: np.ndarray = None) -> float:
        count = self.size
        somme = 0.0
        inds = self.indexes
        data = self.store.data
        if curindexes is not None:
            inds = curindexes
        for i in range(1, count, 1):
            ii = int(inds[i - 1])
            jj = int(inds[i])
            somme += data[ii, jj]
        if curindexes is None:
            self.criteria = somme
        return somme

    def shuffle(self):
        StatIndex.shuffle(self)
        self.compute_criteria()

    def __compute_best_starts(self) -> list[tuple[int, int]]:
        vret = []
        n = self.size
        fbest = 0.0
        data = self.store.data
        pind = self.indexes
        for i in range(n):
            ifirst = int(pind[i])
            for j in range(i):
                if i != j:
                    isecond = int(pind[j])
                    f = data[ifirst, isecond]
                    if f > 0.0:
                        if len(vret) < 1:
                            fbest = f
                            vret = [(ifirst, isecond)]
                        elif (f > 0) and (f < fbest):
                            fbest = f
                            vret = [(ifirst, isecond)]
                        elif f == fbest:
                            vret.append((ifirst, isecond))
        return vret

    def __arrange_step(self, ifirst: int, isecond: int) -> StatIndex:
        pind = self.indexes
        cur = [ifirst, isecond]
        left = []
        for ival in pind:
            if (ival != ifirst) and (ival != isecond):
                left.append(ival)
        data = self.store.data
        while len(left) > 0:
            ncur = len(cur)
            nleft = len(left)
            nm1 = ncur - 1
            pairs = []
            fmin = 0.0
            for i in range(nleft):
                vileft = left[i]
                for j in range(ncur):
                    vjcur = cur[j]
                    fcur = data[vileft, vjcur]
                    if (j == 0) or (j == nm1):
                        fval = fcur
                    else:
                        vjprev = cur[j - 1]
                        f1 = data[vjprev, vileft]
                        f3 = data[vjprev, vjcur]
                        fval = f1 + fcur - f3
                    if len(pairs) < 1 or fval < fmin:
                        fmin = fval
                        pairs = [(i, j)]
                    elif fval == fmin:
                        pairs.append((i, j))
            npl = len(pairs)
            if npl < 1:
                break
            ipos = 0
            if npl > 1:
                ipos = randrange(0, npl)
            cc = pairs[ipos]
            jsecond = cc[1]
            vleft = left[cc[0]]
            if jsecond == 0:
                cur.insert(0, vleft)
            elif jsecond == nm1:
                cur.append(vleft)
            else:
                cur.insert(jsecond, vleft)
            left.remove(vleft)
        n = len(cur)
        vret = np.zeros(n, dtype=int)
        for i in range(n):
            vret[i] = cur[i]
        crit = self.compute_criteria(vret)
        retval = StatIndex()
        retval.initialize_index(crit, vret)
        return retval
