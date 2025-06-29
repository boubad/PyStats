import numpy as np


# ===================
def compute_bertin_classes(
    data: np.ndarray, nclasses: int = 5, brefmedian: bool = False
) -> tuple[list[int], list[float]]:
    if data.ndim != 1:
        raise ValueError("Input data must be a 1D array.")
    n = data.size
    if nclasses < 2 or nclasses > n:
        raise ValueError(
            "Number of classes must be between 2 and the number of data points."
        )
    if n < 2:
        raise ValueError("Input data must contain at least two element.")
    vmin = data.min()
    vmax = data.max()
    if vmin >= vmax:
        raise ValueError("Minimum value must be less than maximum value.")
    if brefmedian:
        # Use median as the reference value
        vmean = np.median(data)
    else:
        # Use mean as the reference value
        if n == 1:
            vmean = data[0]
        else:
            vmean = data.mean()
    # ensure odd classes number
    if nclasses % 2 == 0:
        nclasses += 1
    nc2 = nclasses // 2
    fconst = 2.0 / (nclasses + 1.0)
    infdelta = (vmean - vmin) * fconst
    supdelta = (vmax - vmean) * fconst
    x1 = vmean - (infdelta / 2.0)
    x2 = vmean + (supdelta / 2.0)
    limits = [x1, x2]
    icur = 0
    while x1 > vmin:
        x1 -= infdelta
        if x1 < vmin:
            x1 = vmin
        icur += 1
        if icur == nc2:
            x1 = vmin  # Ensure we do not go below vmin
        limits.insert(0, x1)
    icur = 0
    while x2 < vmax:
        x2 += supdelta
        if x2 > vmax:
            x2 = vmax
        icur += 1
        if icur == nc2:
            x2 = vmax
        limits.append(x2)
    # Ensure we have nclasses + 1 limits
    nc = len(limits)
    if nc != nclasses + 1:
        raise ValueError(
            "Not enough classes generated. Increase the number of classes or check the data range."
        )
    classes = []
    for i in range(n):
        x = data[i]
        bfound = False
        for j in range(nclasses):
            y = limits[j + 1]
            if x > y:
                continue
            classes.append(j + 1)
            bfound = True
            break
        if not bfound:
            classes.append(nclasses)  # Last class for values >= vmax
    return classes, limits


# ===================
def bertin_classes(
    data: np.ndarray, nclasses: int = 5, brefmedian: bool = False
) -> list[int]:
    return compute_bertin_classes(data, nclasses, brefmedian)[0]


# ===================
def compute_outliers(adata:np.ndarray) -> tuple[list[int], list[int]]:
    if adata.ndim != 2:
        raise ValueError("Input data must be a 2D array.")
    res = []
    nrows = adata.shape[0]
    nvars = adata.shape[1]
    for ivar in range(nvars):
        data = adata[:, ivar]
        q25 = np.percentile(data, 25)
        q75 = np.percentile(data, 75)
        cut_off = 1.5 * (q75 - q25)
        lower = q25 - cut_off
        upper = q75 + cut_off
        for i in range(len(data)):
            x = data[i]
            if (x < lower) or (x > upper):
                if i not in res:
                    res.append(i)
    keep = []
    for i in range(nrows):
        if i not in res:
            keep.append(i)
    return (keep, res)


def get_outliers_dict(adata:np.ndarray) -> dict:
    if adata.ndim != 2:
        raise ValueError("Input data must be a 2D array.")
    res = {}
    nvars = adata.shape[1]
    for ivar in range(nvars):
        data = adata[:, ivar]
        q25 = np.percentile(data, 25)
        q75 = np.percentile(data, 75)
        cut_off = 1.5 * (q75 - q25)
        lower = q25 - cut_off
        upper = q75 + cut_off
        cur = []
        for i in range(len(data)):
            x = data[i]
            if (x < lower) or (x > upper):
                cur.append(i)
        if len(cur) > 0:
            res[ivar] = cur
    return res
