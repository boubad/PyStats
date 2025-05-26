import numpy as np

# ===================
def bertin_classes(data: np.ndarray, nclasses: int = 5) -> list[int]:
    if data.ndim != 1:
        raise ValueError("Input data must be a 1D array.")
    if nclasses < 1 or nclasses > 9:
        raise ValueError("Number of classes must be between 1 and 9.")
    n = data.size
    if n == 0:
        return []
    vmin = data.min()
    vmax = data.max()
    if vmin >= vmax:
         return []
    if nclasses == 1:
        return [1] * n  # All values in the same class
    vmean = data.mean()
    # ensure odd classes number
    if nclasses % 2 == 0:
        nclasses += 1
    nc2 = nclasses // 2
    infdelta = (vmean - vmin) / nc2
    supdelta = (vmax - vmean) / nc2
    x1 = vmean - (infdelta/2)
    limits = []
    while x1 >= vmin:
        limits.insert(0, x1)
        x1 -= infdelta
        if x1 < vmin:
            limits.insert(0, vmin)
            break
    x2 = vmean + (supdelta/2)
    while x2 <= vmax:
        limits.append(x2)
        x2 += supdelta
        if x2 > vmax:
            limits.append(vmax)
            break
    nc = len(limits)
    nc1 = nc - 1
    classes = []
    flimits = np.array(limits, dtype=float)
    for i in range(n):
        x = data[i] 
        bfound = False
        for j in range(nc1):
            y1 = flimits[j]
            y2 = limits[j + 1]
            if x >= y1 and x < y2:
                classes.append(j + 1)
                bfound = True
                break
        if not bfound:
            classes.append(nc)  # Last class for values >= vmax

    return classes
