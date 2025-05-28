import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from info import distanceutils

# =================
import numpy as np


# DistanceUtils Test Case
class DistanceUtilsTestCase(unittest.TestCase):
    def test_compute_distance_array(self):
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], dtype=float)
        result = distanceutils.DistanceUtils.compute_distance_array(data, smetric="manhattan", axis=0)
        expected = np.array([[0.0, 9.0, 18.0], [9.0, 0.0, 9.0], [18.0, 9.0, 0.0]], dtype=float)
        np.testing.assert_array_almost_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
