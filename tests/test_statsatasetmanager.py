import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from tests.fixture import TestFixture
import pandas as pd
from info import statdatasetmanager


# =======================
# StatDatasetManager Test Case
# ========================
class TestStatDatasetManager(unittest.TestCase):
    def setUp(self):
        self.manager = statdatasetmanager.StatDatasetManager()
        self.dataset_name = "test_dataset"

    def test_import(self):
        man = self.manager
        f = TestFixture()
        csvfilename = f.csv_filepath
        df = pd.read_csv(csvfilename)
        # print(df)
        oset = man.find_dataset_by_name(self.dataset_name)
        if oset is None:
            bret = man.import_from_dataframe(df, self.dataset_name, indexcol="NOM")
            self.assertTrue(bret)


if __name__ == "__main__":
    unittest.main()
