__author__ = 'VGN'

import unittest
import random


class MinHeap:
    """ class to capture the minheap data structure
    """

    def __init__(self):
        self._heap_list = list()
        self._heap_list.append(-1) # index 0 is not used , root at index 1
        self._size = 0
        self._mapping_dict = {} # dictionary for delete operation with index as "vertex", key - "position in the heap_list"

    def insert(self, item):
        self._size += 1
        # insert item at end of the list
        self._heap_list.append(item)
        self._mapping_dict[item] = self._size
        self._bubble_up(self._size)

    def peek_min(self):
        self._check_for_empty_heap()
        return self._heap_list[1]

    def extract_min(self):
        self._check_for_empty_heap()
        min = self._heap_list[1]
        #swap root with last element
        self._heap_list[1] = self._heap_list[self._size]
        self._heap_list.pop()
        if self._size != 1:
            self._mapping_dict[self._heap_list[1]] = 1
        if min in self._mapping_dict:
            del self._mapping_dict[min]
        self._size -= 1
        self._bubble_down(1) # bubble down from root
        return min

    def delete_at_index(self, index):
        self._check_for_empty_heap()
        if self._size < index:
            raise Exception("No element present to delete at specified index")
        element = self._heap_list[index]
        self._heap_list[index] = self._heap_list[self._size]
        self._mapping_dict[self._heap_list[index]] = index
        self._heap_list.pop()
        self._size -= 1
        if element in self._mapping_dict:
            del self._mapping_dict[element]
        self._bubble_up(index)
        self._bubble_down(index)

    def is_empty(self):
        return self._size == 0

    def get_index_of_element(self, element):
        if element in self._mapping_dict:
            return self._mapping_dict[element]
        else:
            return -1

    def get_element_from_index(self, index):
        if index >=1 and index <= self._size:
            return self._heap_list[index]
        raise Exception("invalid index")

    def _check_for_empty_heap(self):
        if self._size == 0:
            raise Exception("Cannot extract min from empty heap")

    def _bubble_up(self, value):
        """internal method invoked during insert to bubble up the element from the specified index upto root
        until heap property satisfied"""
        # check for violation of heap property
        if self._size <= 1 or value > self._size:
            return
        while value != 1: # bubble up until the root
            element = self._heap_list[value]
            parent = self._heap_list[value/2]
            if element < parent:
                #swap the element with its parent
                self._heap_list[value] = parent
                self._heap_list[value/2] = element
                self._mapping_dict[parent] = value
                self._mapping_dict[element] = value/2
            value = value/2

    def _bubble_down(self, value):
        """internal method invoked during extract_min to bubble down element from specfied index upto leaf
            until heap property satisfied"""
        if self._size <= 1 or value > self._size:
            return
        while 2 * value <= self._size: # check to make sure element is not leaf
            element = self._heap_list[value]
            left_child = self._heap_list[2*value]
            if 2 * value + 1 > self._size:
                right_child = None
            else:
                right_child = self._heap_list[2*value+1]
            if right_child is not None:
                if left_child <= right_child :
                    if element > left_child:
                    #swap element with left child
                        self._heap_list[value] = left_child
                        self._heap_list[2*value] = element
                        self._mapping_dict[left_child] = value
                        self._mapping_dict[element] = 2 * value
                        value = 2*value
                    else:
                        return
                else: #right_child < left_child
                    if element > right_child:
                    #swap element with right child
                        self._heap_list[value] = right_child
                        self._heap_list[2*value+1] = element
                        self._mapping_dict[right_child] = value
                        self._mapping_dict[element] = 2 * value + 1
                        value = 2*value+1
                    else:
                        return
            else: #right_child is None:
                if element > left_child:
                #swap element with left child
                    self._heap_list[value] = left_child
                    self._heap_list[2*value] = element
                    self._mapping_dict[left_child] = value
                    self._mapping_dict[element] = 2 * value
                    value = 2*value
                else:
                    # heap property satisfied can return from while loop
                    return


class HeapTest(unittest.TestCase):
    """Test class for verifying heap data structure"""

    def test_minheap(self):
        lower_bound = 0
        upper_bound = 10
        min_heap = MinHeap()
        random_list = list()
        min_heap_list = list()
        for i in range(lower_bound, upper_bound):
            random_no = random.randint(1,100)
            random_list.append(random_no)
            min_heap.insert(random_no)
        for i in range(lower_bound, upper_bound):
            min_heap_list.append(min_heap.extract_min())
            #print "Min heap list {}".format(min_heap._heap_list)
            #print "Min heap dict {}".format(min_heap._mapping_dict)
        self.assertTrue(sorted(random_list) == min_heap_list)


if __name__ == '__main__':
    unittest.main()





