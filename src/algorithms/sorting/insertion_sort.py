from unittest import TestCase, main as umain


def insertion_sort[T](arr: list[T]) -> list[T]:
    n = len(arr)

    for i in range(1, n):
        insert_idx = i
        current_val = arr.pop(i)

        for j in range(i - 1, -1, -1):
            if arr[j] > current_val:
                insert_idx = j

        arr.insert(insert_idx, current_val)

    return arr


class TestInsertionSort(TestCase):
    def test_insertion_sort(self):
        arr = [10, 8, 9, 7, 33, 45, 68, 91]

        arr_target = arr.copy()
        arr_target.sort()

        self.assertEqual(insertion_sort(arr), arr_target)


if __name__ == '__main__':
    umain()
