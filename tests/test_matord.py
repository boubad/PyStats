import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from info.matord import MatOrd
from info.matriceitemtype import MatriceItemType
from tests.fixture import TestFixture


class TestMatOrd(unittest.TestCase):
    def test_read_csv(self):
        f = TestFixture()
        csvfilename = f.csv_filepath
        omat = MatOrd()
        b = omat.read_csv(csvfilename, robust=True)
        self.assertTrue(b)
        omat.partition()
        print(
            "\nINITIAL STATE\nROWINDEX:{}\nCOLINDEX:{}\nCOLS: {}\nROWS: {}\nDATA:{}\n".format(
                omat.rowindex, omat.colindex, omat.varnames, omat.indnames, omat.data
            )
        )
        omat.arrange(metric="manhattan", mode=MatriceItemType.ROWCOL)
        print(
            "\nFINAL STATE\nROWINDEX:{}\nCOLINDEX:{}\nCOLS: {}\nROWS: {}\nDATA:{}\n".format(
                omat.rowindex, omat.colindex, omat.varnames, omat.indnames, omat.data
            )
        )


if __name__ == "__main__":
    unittest.main()
