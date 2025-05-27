import numpy as np


# ===================
def bertin_classes(data: np.ndarray, nclasses: int = 5) -> list[int]:
    if data.ndim != 1:
        raise ValueError("Input data must be a 1D array.")
    n = data.size
    if n == 0:
        return []
    if nclasses < 1 or nclasses > n:
        raise ValueError(
            "Number of classes must be between 1 and the number of data points."
        )
    vmin = data.min()
    vmax = data.max()
    if vmin >= vmax:
        raise ValueError("Minimum value must be less than maximum value.")
    if nclasses == 1:
        return [1] * n  # All values in the same class
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
    icur = 0
    limits = [x1, x2]
    while x1 > vmin:
        x1 -= infdelta
        if x1 > vmin:
            icur += 1
            if icur < nc2:
                limits.insert(0, x1)
            else:
                limits.insert(0, vmin)
                break
    icur = 0
    while x2 < vmax:
        x2 += supdelta
        if x2 < vmax:
            icur += 1
            if icur < nc2:
                limits.append(x2)
            else:
                limits.append(vmax)
                break
    nc = len(limits)
    if nc < nclasses:
        raise ValueError(
            "Not enough classes generated. Increase the number of classes or check the data range."
        )
    classes = []
    flimits = np.array(limits, dtype=float)
    for i in range(n):
        x = data[i]
        bfound = False
        for j in range(nclasses):
            y = flimits[j + 1]
            if x > y:
                continue
            classes.append(j + 1)
            bfound = True
            break
        if not bfound:
            classes.append(nclasses)  # Last class for values >= vmax
    return classes
