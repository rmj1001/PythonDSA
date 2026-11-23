from unittest import TestCase, main as umain


def swap[T](arr: list[T], index1: int, index2: int) -> None:
    """Swap two elements in-place in an array"""
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp


def find_min[T](arr: list[T], start_index: int) -> int:
    min_index = start_index
    size = len(arr)

    for current_index in range(start_index + 1, size, 1):
        if arr[min_index] > arr[current_index]:
            min_index = current_index

    return min_index


def selection_sort[T](arr: list[T]) -> list[T]:
    size = len(arr)
    for start_index in range(0, size - 1, 1):
        min_index = find_min(arr, start_index)
        swap(arr, min_index, start_index)

    return arr


class TestSelectionSort(TestCase):
    def test_selection_sort(self):
        arr = [10, 8, 9, 7, 33, 45, 68, 91]

        arr_target = arr.copy()
        arr_target.sort()

        self.assertEqual(selection_sort(arr), arr_target)


if __name__ == '__main__':
    umain()
