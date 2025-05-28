import math
import numpy as np


class DistanceUtils(object):
    def compute_distance_array(
        initialdata: np.ndarray,
        metric: str = "manhattan",
        axis: int = 0,
        weights: np.ndarray = None,
    ) -> np.ndarray | None:
        if (
            (initialdata is not None)
            and isinstance(initialdata, np.ndarray)
            and initialdata.ndim == 2
        ):
            nrows = initialdata.shape[0]
            ncols = initialdata.shape[1]
            if axis == 0 and nrows > 1 and ncols > 0:
                vret = np.zeros((nrows, nrows))
                for i in range(nrows):
                    ind = initialdata[i, :]
                    for j in range(i):
                        if i > j:
                            y = initialdata[j, :]
                            x = DistanceUtils.distance(ind, y, metric, weights)
                            vret[i, j] = x
                            vret[j, i] = x
                return vret
            elif axis == 1 and ncols > 1 and nrows > 0:
                vret = np.zeros((ncols, ncols))
                for i in range(ncols):
                    ind = initialdata[:, i]
                    for j in range(i):
                        if i > j:
                            y = initialdata[:, j]
                            x = DistanceUtils.distance(ind, y, metric, weights)
                            vret[i, j] = x
                            vret[j, i] = x
                return vret
        return None

    def get_all_metrics() -> list[str]:
        return [
            "euclidian",
            "manhattan",
            "maximum",
            "jaccard",
            "canberra",
            "binary",
        ]

    def distance(
        data1: np.ndarray,
        data2: np.ndarray,
        metric: str = "manhattan",
        weights: np.ndarray = None,
    ) -> float:
        if (data1 is None) or (data2 is None):
            raise ValueError("invalid input parameter")
        if (not isinstance(data1, np.ndarray)) or (not isinstance(data2, np.ndarray)):
            raise ValueError("invalid input type")
        if data2.ndim != data1.ndim or data1.ndim != 1:
            raise ValueError("invalid input dimension")
        if metric not in DistanceUtils.get_all_metrics():
            raise ValueError("invalid metric")
        if weights is not None:
            if not isinstance(weights, np.ndarray):
                raise ValueError("invalid weights type")
            if weights.ndim != 1:
                raise ValueError("invalid weights dimension")
            if weights.size != data1.size:
                raise ValueError("invalid weights size")
        if metric == "manhattan":
            return DistanceUtils.manhattan_distance(data1, data2, weights)
        elif metric == "maximum":
            return DistanceUtils.maximum_distance(data1, data2, weights)
        elif metric == "jaccard":
            return DistanceUtils.jaccard_distance(data1, data2)
        elif metric == "canberra":
            return DistanceUtils.canberra_distance(data1, data2)
        elif metric == "binary":
            return DistanceUtils.binary_distance(data1, data2)
        return DistanceUtils.euclidian_distance(data1, data2, weights)

    def euclidian_distance(
        data1: np.ndarray, data2: np.ndarray, w: np.ndarray = None
    ) -> float:
        t = data1 - data2
        t = t * t
        if w is not None:
            t = t * w
            return math.sqrt(t.sum() / w.sum())
        else:
            return math.sqrt(t.sum())

    def manhattan_distance(
        data1: np.ndarray, data2: np.ndarray, w: np.ndarray = None
    ) -> float:
        t = abs(data1 - data2)
        if w is not None:
            t = t * w
            return t.sum() / w.sum()
        else:
            return t.sum()

    def maximum_distance(
        data1: np.ndarray, data2: np.ndarray, w: np.ndarray = None
    ) -> float:
        n = data1.size
        v = 0
        if w is not None:
            for i in range(n):
                x = abs(data1[i] - data2[i]) * w[i]
                if (i == 0) or (x > v):
                    v = x
            return v
        else:
            for i in range(n):
                x = abs(data1[i] - data2[i])
                if (i == 0) or (x > v):
                    v = x
            return v

    def jaccard_distance(data1: np.ndarray, data2: np.ndarray) -> float:
        n = data1.size
        v = 0
        d = 0
        for i in range(n):
            x1 = data1[i]
            x2 = data2[i]
            v += x1 if (x1 < x2) else x2
            d += x1 if (x1 > x2) else x2
        if d != 0:
            return 1.0 - (v / d)
        else:
            raise ValueError("invalid input parameter")

    def canberra_distance(data1: np.ndarray, data2: np.ndarray) -> float:
        n = data1.size
        v = 0
        for i in range(n):
            x1 = data1[i]
            x2 = data2[i]
            if (x1 > 0) or (x2 > 0):
                nx = abs(x1 - x2)
                ny = abs(x1) + abs(x2)
                v += nx / ny
        return v

    def binary_distance(
        data1: np.ndarray, data2: np.ndarray, limit: float = 0.0
    ) -> float:
        n = data1.size
        v = 0
        d = 0
        for i in range(n):
            x1 = float(data1[i]) > limit
            x2 = float(data2[i]) > limit
            if x1 and x2:
                v += 1.0
            if x1 or x2:
                d += 1.0
        if d != 0:
            return 1.0 - (v / d)
        else:
            raise ValueError("invalid input parameter")
