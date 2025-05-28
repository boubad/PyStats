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
    def setUp(self):
        self.index = statindex.StatIndex(3)

    def test_initialization(self):
        self.assertEqual(self.index.size, 3)
        self.assertEqual(self.index.criteria, 1.0)
        self.assertListEqual(self.index.indexes, [0, 1, 2])

    def test_str(self):
        expected = '{"criteria":1.0, "indexes":[0, 1, 2]}'
        self.assertEqual(str(self.index), expected)

    def test_getitem(self):
        self.assertEqual(self.index[1], 1)

    def test_setitem(self):
        self.index[1] = 5
        self.assertEqual(self.index[1], 5)

    def test_add(self):
        other = statindex.StatIndex(3, crit=2.0)
        new_index = self.index + other
        self.assertIsInstance(new_index, statindex.StatIndex)

    def test_len(self):
        self.assertEqual(len(self.index), 3)

    def test_eq(self):
        other = statindex.StatIndex(3, crit=1.0)
        self.assertTrue(self.index == other)

    def test_le(self):
        other = statindex.StatIndex(3, crit=1.0)
        self.assertTrue(self.index <= other)

    def test_lt(self):
        other = statindex.StatIndex(3, crit=2.0)
        self.assertTrue(self.index < other)

    def test_valid_property(self):
        self.assertTrue(self.index.valid)

    def test_size_property(self):
        self.assertEqual(self.index.size, 3)

    def test_criteria_property(self):
        self.assertEqual(self.index.criteria, 1.0)

    def test_indexes_property(self):
        self.assertListEqual(self.index.indexes, [0, 1, 2])

    def test_is_valid_indexes(self):
        valid_indexes = np.array([0, 1, 2])
        invalid_indexes = np.array([0, 1, 3])
        self.assertTrue(statindex.StatIndex.is_valid_indexes(valid_indexes))
        self.assertFalse(statindex.StatIndex.is_valid_indexes(invalid_indexes))

    def test_is_equal(self):
        other = statindex.StatIndex(3, crit=1.0)
        self.assertTrue(self.index.is_equal(other))
        other = statindex.StatIndex(3, crit=1.0)
        self.assertFalse(self.index.is_equal(other))

    def test_is_less_than(self):
        other = statindex.StatIndex(3, crit=1.0)
        self.assertFalse(self.index.is_less_than(other))
        other = statindex.StatIndex(3, crit=1.0)
        self.assertTrue(self.index.is_less_than(other))

    def test_add_indexes(self):
        other = statindex.StatIndex(3, crit=2.0)
        new_index = self.index + other
        self.assertIsInstance(new_index, statindex.StatIndex)

    def test_clone(self):
        clone = self.index.clone()
        self.assertEqual(clone.size, self.index.size)
        self.assertEqual(clone.criteria, self.index.criteria)
        np.testing.assert_array_equal(clone.indexes, self.index.indexes)

    def test_resize(self):
        self.index.resize(5)
        self.assertEqual(self.index.size, 5)
        self.assertListEqual(self.index.indexes.tolist(), [0, 1, 2, 0, 0])
        self.index.resize(0)
        self.assertEqual(self.index.size, 0)
        self.assertIsNone(self.index.indexes)

    def test_shuffle(self):
        original_indexes = self.index.indexes.copy()
        self.index.shuffle()
        self.assertNotEqual(original_indexes.tolist(), self.index.indexes.tolist())
        self.assertTrue(
            np.array_equal(np.sort(self.index.indexes), np.arange(self.index.size))
        )

    def test_get_index_at(self):
        self.assertEqual(self.index.get_index_at(1), 1)
        with self.assertRaises(ValueError):
            self.index.get_index_at(3)
        with self.assertRaises(ValueError):
            self.index.get_index_at(-1)

    def test_is_reverse(self):
        other = statindex.StatIndex(3, crit=1.0)
        self.assertTrue(self.index.is_reverse(other))
        other = statindex.StatIndex(3, crit=1.0)
        self.assertFalse(self.index.is_reverse(other))

    def test_is_reverse_invalid(self):
        other = None
        self.assertFalse(self.index.is_reverse(other))
        other = "not a StatIndex"
        self.assertFalse(self.index.is_reverse(other))
        other = statindex.StatIndex(3, crit=1.0)
        self.assertFalse(self.index.is_reverse(other))


if __name__ == "__main__":
    unittest.main()
