import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from info import statindex
import numpy as np


# ==============
# StatIndex Test Case
# ==============
class TestStatIndex(unittest.TestCase):
    def test_is_valid_indexes(self):
        self.assertTrue(statindex.StatIndex.is_valid_indexes(np.array([0, 1, 2])))
        self.assertFalse(statindex.StatIndex.is_valid_indexes(np.array([0, 1, 3])))
        self.assertFalse(statindex.StatIndex.is_valid_indexes(np.array([-1, 0, 1])))
        self.assertFalse(statindex.StatIndex.is_valid_indexes(np.array([0, 1, 2, 2])))
        self.assertFalse(statindex.StatIndex.is_valid_indexes(None))
        self.assertFalse(statindex.StatIndex.is_valid_indexes(np.array([])))

    def test_initialization(self):
        si = statindex.StatIndex(the_size=5)
        self.assertEqual(si.size, 5)
        self.assertTrue(si.valid)

    def test_resize(self):
        si = statindex.StatIndex(the_size=3)
        si.resize(5)
        self.assertEqual(si.size, 5)
        self.assertTrue(si.valid)

    def test_criteria(self):
        si = statindex.StatIndex(crit=0.5)
        self.assertEqual(si.criteria, 0.5)

    def test_str(self):
        si = statindex.StatIndex(the_size=3)
        expected_str = '{"criteria":0.0, "indexes":[0, 1, 2]}'
        self.assertEqual(str(si), expected_str)

   

if __name__ == "__main__":
    unittest.main()
