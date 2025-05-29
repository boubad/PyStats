import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
import numpy as np
from info import distancestore


# ==============
# DistanceStore Test Case
# ==============
class TestDistanceStore(unittest.TestCase):
    def test_initialization(self):
        ds = distancestore.DistanceStore(5)
        self.assertEqual(ds.size, 5)
        self.assertTrue(ds.valid)

    def test_invalid_initialization(self):
        ds = distancestore.DistanceStore(-1)
        self.assertEqual(ds.size, 0)
        self.assertFalse(ds.valid)

    def test_str(self):
        ds = distancestore.DistanceStore(3)
        expected_str = "DistanceStore size: 3"
        self.assertEqual(str(ds), expected_str)

    def test_initialize_test(self):
        ds = distancestore.DistanceStore()
        ds.initialize_test(4)
        self.assertTrue(ds.valid)
        self.assertEqual(ds.size, 4)
        expected_data = np.array(
            [
                [0.0, 1.0, 2.0, 3.0],
                [1.0, 0.0, 1.0, 2.0],
                [2.0, 1.0, 0.0, 1.0],
                [3.0, 2.0, 1.0, 0.0],
            ]
        )
        np.testing.assert_array_equal(ds.data, expected_data)

    def test_data_property(self):
        ds = distancestore.DistanceStore(3)
        self.assertIsNotNone(ds.data)
        self.assertEqual(ds.data.shape, (3, 3))
        self.assertTrue(np.all(ds.data == 0))

        new_data = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
        ds.data = new_data
        np.testing.assert_array_equal(ds.data, new_data)

        with self.assertRaises(ValueError):
            ds.data = np.array([1, 2])

    def test_invalid_data(self):
        ds = distancestore.DistanceStore(3)
        with self.assertRaises(ValueError):
            ds.data = np.array([1, 2])

    def test_size_property(self):
        ds = distancestore.DistanceStore(4)
        self.assertEqual(ds.size, 4)
        ds.data = np.array([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]])
        self.assertEqual(ds.size, 4)

        ds = distancestore.DistanceStore(0)
        self.assertEqual(ds.size, 0)
        self.assertFalse(ds.valid)


if __name__ == "__main__":
    unittest.main()
