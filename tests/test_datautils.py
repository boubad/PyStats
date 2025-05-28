import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from info import datautils
import numpy as np


# ============
# Test for bertin_classes function in datautils module
class TestBertinClasses(unittest.TestCase):
    def test_bertin_classes(self):
        # Test with a simple case
        data = np.array([1, 2, 3, 4, 5])
        result = datautils.bertin_classes(data, nclasses=3)
        expected = [1, 1, 2, 3, 3]
        self.assertEqual(result, expected)

        # Test with brefmedian set to True
        result = datautils.bertin_classes(data, nclasses=3, brefmedian=True)
        self.assertEqual(result, expected)

        # Test with a single value
        data = np.array([42])
        with self.assertRaises(ValueError):
            datautils.bertin_classes(data, nclasses=1)

        # Test with invalid nclasses
        data = np.array([1, 2, 3, 4, 5])
        with self.assertRaises(ValueError):
            datautils.bertin_classes(data, nclasses=0)


# ==========


if __name__ == "__main__":
    unittest.main()
