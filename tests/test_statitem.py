import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
from info import statitem
import numpy as np


#  =======
# StatItem Test Case
#  =======
class TestStatItem(unittest.TestCase):
    def setUp(self):
        self.item = statitem.StatItem(1, "test", 5)

    def test_initialization(self):
        self.assertEqual(self.item.index, 1)
        self.assertEqual(self.item.name, "test")
        self.assertEqual(self.item.size, 5)

    def test_str(self):
        expected = '{"index":1, "name": "test", "data": [0.0, 0.0, 0.0, 0.0, 0.0]}'
        self.assertEqual(str(self.item), expected)

    def test_clone(self):
        clone = self.item.clone()
        self.assertEqual(clone.index, self.item.index)
        self.assertEqual(clone.name, self.item.name)
        np.testing.assert_array_equal(clone.data, self.item.data)

    def test_distance(self):
        other = statitem.StatItem(2, "test2", 5)
        np.random.seed(0)
        self.item.data = np.random.rand(5)
        other.data = np.random.rand(5)
        dist = self.item.distance(other)
        self.assertIsInstance(dist, float)

    def test_resize(self):
        self.item.resize(10)
        self.assertEqual(self.item.size, 10)
        self.assertIsNotNone(self.item.data)
        np.testing.assert_array_equal(self.item.data, np.zeros(10, dtype=float))

    def test_status(self):
        self.assertEqual(self.item.status, statitem.StatItemStatusType.ACTIVE)
        self.item.status = statitem.StatItemStatusType.INACTIVE
        self.assertEqual(self.item.status, statitem.StatItemStatusType.INACTIVE)

    def test_valid(self):
        self.assertTrue(self.item.valid)
        self.item.data = None
        self.assertFalse(self.item.valid)

    def test_size(self):
        self.assertEqual(self.item.size, 5)
        self.item.resize(0)
        self.assertEqual(self.item.size, 0)
        self.assertIsNone(self.item.data)


if __name__ == "__main__":
    unittest.main()
