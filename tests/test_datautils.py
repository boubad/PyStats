import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import unittest
from info import datautils
import numpy as np
# ==========
class TestDataUtils(unittest.TestCase):
    def test_bertin_classes(self):
        # Test with a simple 1D array
        data = np.random.random(10)
        classes = datautils.bertin_classes(data, nclasses=5)
        nc = len(classes)
        self.assertEqual(nc, 10)
        self.assertEqual(classes, [1, 2, 3])
