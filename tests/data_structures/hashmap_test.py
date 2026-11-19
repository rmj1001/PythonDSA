import unittest
from unittest import TestCase

from src.data_structures.hashmap import HashMap, HashMapError


class TestHashMap(TestCase):
    def test_repr(self):
        hm = HashMap()
        hm.set('Roy', 'Alice')

        self.assertEqual(
            str(hm),
            'HashMap\n{\n\tRoy: Alice\n}\n'
        )

    def test_insert(self):
        hm = HashMap()

        hm.set('Roy', 'Alice')

        self.assertEqual(hm.get('Roy', 'None'), 'Alice')

    def test_get(self):
        hm = HashMap()

        hm.set('Roy', 'Alice')

        self.assertEqual(hm.get('Roy', 'None'), 'Alice')

        with self.assertRaises(HashMapError):
            hm.get('Timmy')

    def test_remove(self):
        hm = HashMap()

        hm.set('Roy', 'Alice')

        hm.remove('Roy')

        with self.assertRaises(HashMapError):
            hm.remove('Timmy')


if __name__ == '__main__':
    unittest.main()
