from unittest import TestCase, main as umain


def swap[T](arr: list[T], index1: int, index2: int) -> None:
    """Swap two elements in-place in an array"""
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp


def bubble_up[T](arr: list[T], top_index: int) -> list[T]:
    for j in range(0, top_index, 1):
        if arr[j] > arr[j + 1]:
            swap(arr, j, j + 1)

    return arr


def bubble_sort[T](arr: list[T]) -> list[T]:
    size = len(arr)
    top_index = size - 1

    # At each iteration, the largest element is "bubbled up"
    while top_index >= 1:
        arr = bubble_up(arr, top_index)
        top_index -= 1

    return arr


class TestBubbleSort(TestCase):
    def test_bubble_sort(self):
        arr = [10, 8, 9, 7, 33, 45, 68, 91]
        arr2 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        arr_target = arr.copy()
        arr_target.sort()

        arr2_target = arr2.copy()
        arr2_target.sort()

        self.assertEqual(bubble_sort(arr), arr_target)
        self.assertEqual(bubble_sort(arr2), arr2_target)


if __name__ == '__main__':
    umain()
