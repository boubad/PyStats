import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from info.statdataset import StatDataset
from tests.fixture import TestFixture


class TestStatDataset(unittest.TestCase):
    def test_get_array_full(self):
        f = TestFixture()
        csvfilename = f.csv_filepath_full
        oset = StatDataset()
        oset.read_csv(csvfilename, hasnames=False)
        self.assertTrue(oset.valid)
        nrows = oset.rows
        ncols = oset.cols
        print("\nROWS: {}\tCOLS: {}".format(nrows, ncols))

    def test_get_array(self):
        f = TestFixture()
        csvfilename = f.csv_filepath
        oset = StatDataset()
        oset.read_csv(csvfilename)
        self.assertTrue(oset.valid)
        dx = oset.data
        print(dx)

    def test_cols_distances(self):
        f = TestFixture()
        csvfilename = f.csv_filepath
        oset = StatDataset()
        b = oset.read_csv(csvfilename)
        self.assertTrue(b)
        b = oset.valid
        self.assertTrue(b)
        # oset.normalize()
        ds = oset.get_cols_distances()
        print(ds)

    def test_categorize(self):
        f = TestFixture()
        csvfilename = f.csv_filepath
        oset = StatDataset()
        b = oset.read_csv(csvfilename)
        self.assertTrue(b)
        b = oset.valid
        self.assertTrue(b)
        oset.partition()
        print(oset.data)


if __name__ == "__main__":
    unittest.main()
