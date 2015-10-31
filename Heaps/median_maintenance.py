__author__ = 'VGN'
import unittest
from heap import MaxHeap
from heap import MinHeap


class MedianMaintenance:
    def __init__(self):
        self.hlow_heap = MaxHeap()
        self.hhigh_heap = MinHeap()

    def compute_median(self, i):
        self.insert_heap(i)
        self.balance_heap()
        return self.median()

    def balance_heap(self):
        if self.hhigh_heap.size - self.hlow_heap.size > 1 : # rebalance heap to keep it balanced
            high = self.hhigh_heap.extract_min()
            self.hlow_heap.insert(high)
        elif self.hlow_heap.size - self.hhigh_heap.size > 1:
            low = self.hlow_heap.extract_max()
            self.hhigh_heap.insert(low)

    def insert_heap(self, i):
        if self.hlow_heap.is_empty():
            low = None
        else:
            low = self.hlow_heap.peek_max()
        if self.hhigh_heap.is_empty():
            high = None
        else:
            high = self.hhigh_heap.peek_min()
        if low is None or i < low:
            self.hlow_heap.insert(i)
        elif high is not None and i > high:
            self.hhigh_heap.insert(i)
        else:# i wedged inbetween insert in first heap by default
            self.hlow_heap.insert(i)

    def median(self):
        if self.hhigh_heap.size - self.hlow_heap.size == 1:
            return self.hhigh_heap.peek_min()
        else:# default choice when hlow is bigger/same size as hhigh
            return self.hlow_heap.peek_max()


class MedianMaintenanceTest(unittest.TestCase):
    """Test class for verifying heap data structure"""

    def compute_median_maintenance(self, file_name):
        tot_sum = 0
        count = 0
        median_maintenance = MedianMaintenance()
        with open(file_name, "r") as ins:
            for line in ins:
                tot_sum += median_maintenance.compute_median(int(line))
                count += 1
        return tot_sum % count

    def test1(self):
        val = self.compute_median_maintenance("median.txt")
        self.assertTrue(val == 1213)


if __name__ == '__main__':
    unittest.main()





