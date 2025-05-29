import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
import numpy as np
from scipy.stats import rankdata
from info.arrangeitem import ArrangeItem
from info.distancestore import DistanceStore
from info.distanceutils import DistanceUtils
from info.partitioner import Partitioner
from tests.fixture import TestFixture


class TestArrangeItem(unittest.TestCase):
    def test_find_tsp(self):
        n = 14
        item = ArrangeItem()
        item.initialize_test(n)
        print("\nINITIAL STATE: {}\n".format(item))
        item.tsp_arrange()
        print("\nARRANGED STATE: {}\n".format(item))

    def test_arrange_tsp_rank(self):
        f = TestFixture()
        ldata = f.read_csv()[2]
        data = np.array(ldata)
        data = rankdata(data, axis=0)
        distance_matrix = DistanceUtils.compute_distance_array(data, smetric="manhattan")
        st = DistanceStore()
        st.data = distance_matrix
        item = ArrangeItem()
        item.store = st
        print("\nINITIAL STATE: {}\n".format(item))
        item.arrange()
        print("\nARRANGED STATE: {}\n".format(item))
        item.tsp_arrange()
        print("\nTSP ARRANGED STATE: {}\n".format(item))

    def test_arrange_tsp(self):
        f = TestFixture()
        ldata = f.read_csv()[2]
        data = np.array(ldata)
        data = Partitioner.partition(data)
        distance_matrix = DistanceUtils.compute_distance_array(data, smetric="manhattan")
        st = DistanceStore()
        st.data = distance_matrix
        item = ArrangeItem()
        item.store = st
        print("\nINITIAL STATE: {}\n".format(item))
        item.arrange()
        print("\nARRANGED STATE: {}\n".format(item))
        item.tsp_arrange()
        print("\nTSP ARRANGED STATE: {}\n".format(item))

    def test_teststore(self):
        n = 20
        item = ArrangeItem()
        item.initialize_test(n)
        nx = item.size
        self.assertEqual(nx, n)
        nn = n * n
        ds = item.store
        data = ds.data
        self.assertEqual(data.size, nn)
        indexes = item.indexes
        self.assertEqual(indexes.size, n)
        print("initial state")
        print(indexes)
        crit = item.compute_criteria()
        self.assertTrue(crit > 0.0)
        print(crit)
        print("final state")
        lret = item.arrange()
        for cur in lret:
            print(cur)


if __name__ == "__main__":
    unittest.main()
