__author__ = 'VGN'
import unittest

from quick_sort import QuickSort
from quick_sort import RSelect
from quick_sort import DSelect


class QuickSortTest(unittest.TestCase):

    def test_quicksort(self):
        input_first = list()
        with open("unsortedArrayFile.txt", "r") as ins:
            for line in ins:
                input_first.append(int(line))
        input_last = input_first[:]
        input_median = input_first[:]
        x = QuickSort(input_first, "first").comparison_count
        self.assertTrue(x == 162085)
        y = QuickSort(input_last, "last").comparison_count
        self.assertTrue(y == 164123)
        z = QuickSort(input_median, "median").comparison_count
        self.assertTrue(z == 138382)

    def test_select(self):
        input_first = list()
        with open("unsortedArrayFile.txt", "r") as ins:
            for line in ins:
                input_first.append(int(line))
        rselect_list = input_first[:]
        dselect_list = input_first[:]
        QuickSort(input_first, "median")
        val1 = RSelect(rselect_list, 50).rselect_val
        self.assertTrue(input_first[50] == val1)
        val2 = DSelect(dselect_list, 50).dselect_val
        self.assertTrue(input_first[50] == val1)


if __name__ == '__main__':
        unittest.main()