import csv


def read_csv(
    filename: str, hasnames: bool = True
) -> tuple[list[str], list[str], list[list[float]]]:
    vinds = []
    vlistdata = []
    vnames = []
    try:
        with open(filename, newline="") as csvfile:
            ncols = 0
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                nx = len(row)
                if nx < 1:
                    continue
                sfirst = (row[0]).strip()
                if len(sfirst) < 1:
                    continue
                if sfirst[0] == "#":
                    continue
                if (ncols > 0) and (nx < ncols):
                    continue
                elif (ncols > 0) and hasnames and (nx < (ncols + 1)):
                    continue
                if ncols < 1:
                    if hasnames:
                        vnames = row[1:]
                    else:
                        vnames = row
                    ncols = len(vnames)
                    continue
                index = len(vinds)
                xdata = [0.0] * ncols
                if hasnames:
                    istart = 1
                    iend = ncols + 1
                    xid = row[0]
                else:
                    istart = 0
                    iend = ncols
                    xid = "ind" + str(index + 1)
                for i in range(istart, iend):
                    s: str = row[i]
                    ss = s.strip()
                    try:
                        x = float(ss)
                        if hasnames:
                            xdata[i - 1] = x
                        else:
                            xdata[i] = x
                    except ValueError:
                        pass
                vinds.append(xid)
                vlistdata.append(xdata)
    except Exception:
        pass
    return vinds, vnames, vlistdata
