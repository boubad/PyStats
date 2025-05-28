import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from info import partitioner
import numpy as np


# =================
# Partitioner Test Case
# =================
class PartitionerTestCase(unittest.TestCase):
    def setUp(self):
        self.data = np.array(
            [
                1.0,
                2.0,
                3.0,
                4.0,
                5.0,
                6.0,
                7.0,
                8.0,
                9.0,
                10.0,
            ]
        )
        self.nbclasses = 5

    def test_init_uniform(self):
        part = partitioner.Partitioner(self.data, self.nbclasses, "uniform")
        self.assertEqual(len(part.limits), 6)
        self.assertEqual(part.limits[0], 1.0)
        self.assertEqual(part.limits[-1], 10.0)
        results = part.categs
        self.assertEqual(len(results), len(self.data))

    def test_init_bertin(self):
        part = partitioner.Partitioner(self.data, self.nbclasses, "bertin")
        self.assertEqual(len(part.limits), 6)
        self.assertEqual(part.limits[0], 1.0)
        self.assertEqual(part.limits[-1], 10.0)
        result = part.categs
        self.assertEqual(len(result), len(self.data))


if __name__ == "__main__":
    unittest.main()
