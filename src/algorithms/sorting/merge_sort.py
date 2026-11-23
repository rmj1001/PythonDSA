from unittest import TestCase, main as umain


def merge[T](left: list[T], right: list[T]) -> list[T]:
    result: list[T] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort[T](arr: list[T]) -> list[T]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    sorted_left = merge_sort(left)
    sorted_right = merge_sort(right)

    return merge(sorted_left, sorted_right)


class TestMergeSort(TestCase):
    def test_merge_sort(self):
        arr = [10, 8, 9, 7, 33, 45, 68, 91]

        arr_target = arr.copy()
        arr_target.sort()

        self.assertEqual(merge_sort(arr), arr_target)


if __name__ == '__main__':
    umain()
