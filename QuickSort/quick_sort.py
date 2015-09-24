__author__ = 'VGN'

import random


class SortUtility:
    """utility class for quick sort/ith order statistic algorithms """
    def __init__(self, input_list):
        self.input_list = input_list

    def choose_pivot(self, input_list,  pos_pivot, start_index, end_index, index=None):
        if pos_pivot == "first":
            index = start_index
        elif pos_pivot == "last":
            index = end_index
        elif pos_pivot == "median":
            middle_index = (end_index - start_index) / 2 + start_index
            median_index = self.pick_median(input_list, start_index, middle_index, end_index)
            index = median_index
        elif pos_pivot == "random":# choose random pivot
            index = random.randint(start_index, end_index)
        tmp = input_list[index]
        input_list[index] = self.input_list[start_index]
        input_list[start_index] = tmp


    def pick_median(self, input_list, start_index, middle_index, end_index):
        start_val = input_list[start_index]
        end_val = input_list[end_index]
        middle_val = input_list[middle_index]
        if end_index - start_index == 1:  # for 2 element array
            if start_val < end_val:
                return start_index
            else:
                return end_index
        if start_val < middle_val < end_val or end_val < middle_val < start_val:
            return middle_index
        elif start_val < end_val < middle_val or middle_val < end_val < start_val:
            return end_index
        elif end_val < start_val < middle_val or middle_val < start_val < end_val:
            return start_index

    def partition(self, input_list, start_index, end_index):
        pivot = input_list[start_index]
        i = start_index + 1
        for j in range(start_index + 1, end_index + 1):
            if input_list[j] < pivot:
                # swap element at j and i and increment i
                tmp = input_list[j]
                input_list[j] = input_list[i]
                input_list[i] = tmp
                i += 1
        # swap pivot with i-1
        tmp = input_list[i - 1]
        input_list[i - 1] = pivot
        input_list[start_index] = tmp
        # return position of pivot in final array
        return i - 1


class QuickSort(SortUtility):
    def __init__(self, input_list, pos_pivot="first"):
        SortUtility.__init__(self, input_list)
        self.comparison_count = 0
        self.pos_pivot = pos_pivot
        self._recursive_quick_sort(self.input_list, 0, len(self.input_list) - 1)

    def _recursive_quick_sort(self, input_list, start_index, end_index):
        if start_index >= end_index:  # base case
            return
        self.comparison_count += end_index - start_index
        self.choose_pivot(input_list, self.pos_pivot, start_index, end_index)
        pivot_pos = self.partition(input_list, start_index, end_index)
        self._recursive_quick_sort(input_list, start_index, pivot_pos - 1)
        self._recursive_quick_sort(input_list, pivot_pos + 1, end_index)


class RSelect(SortUtility):
    def __init__(self, input_list, order_statistic):
        SortUtility.__init__(self, input_list)
        self.rselect_val = self._rselect(input_list, 0, len(self.input_list) - 1, order_statistic)

    def _rselect(self, input_list, start_index, end_index, order_statistic):
        #method to perform the ith order statistic in the array
        if start_index >= end_index: #base case
            return input_list[start_index]
        self.choose_pivot(input_list, "random", start_index, end_index)
        pivot_pos = self.partition(input_list, start_index, end_index)
        if order_statistic == pivot_pos:
            return input_list[pivot_pos]
        if pivot_pos > order_statistic:
            return self._rselect(input_list, start_index, pivot_pos-1, order_statistic)
        if pivot_pos < order_statistic:
            return self._rselect(input_list, pivot_pos+1, end_index, order_statistic)

class DSelect(SortUtility):
    def __init__(self, input_list, order_statistic):
        SortUtility.__init__(self, input_list)
        self.dselect_val = self._dselect(input_list, 0, len(self.input_list) - 1, order_statistic)

    def _dselect(self, input_list,  start_index, end_index, order_statistic):
        #method to perform the ith order statistic in the array
        if start_index >= end_index: #base case
            return input_list[start_index]
        median_val = self._median_dselect(input_list, start_index, end_index, order_statistic)
        pivot_pos = self._get_pivot_pos(median_val, input_list)
        self.choose_pivot(input_list, None, start_index, end_index, pivot_pos)
        pivot_pos = self.partition(input_list, start_index, end_index)
        if order_statistic == pivot_pos:
            return input_list[pivot_pos]
        if pivot_pos > order_statistic:
            return self._dselect(input_list, start_index, pivot_pos-1, order_statistic)
        if pivot_pos < order_statistic:
            return self._dselect(input_list, pivot_pos+1, end_index, order_statistic)

    def _median_dselect(self, input_list, start_index, end_index, order_statistic):
        if start_index >= end_index:
            return input_list[start_index]
        c = self._median_of_medians(input_list, start_index, end_index)
        return self._median_dselect(c, 0, len(c)-1, order_statistic/10)


    def _get_pivot_pos(self, pivot_val, input_list):
        for index in range(0, len(input_list)):
            if input_list[index] == pivot_val:
                return index

    def __insertion_sort(self, input_list, start_index, end_index):
        new_list = input_list[start_index: end_index+1]
        for index in range(0, len(new_list)):
            currentvalue = new_list[index]
            position = index
            while position>0 and new_list[position-1]>currentvalue:
                new_list[position]= new_list[position-1]
                position = position-1
            new_list[position]=currentvalue
        median_index = (len(new_list)-1) / 2
        return new_list[median_index]

    def _median_of_medians(self, input_list, start_index, end_index):
        c = list()
        start_counter = start_index
        end_counter = start_counter + 4
        while end_counter <= end_index:
            c.append(self.__insertion_sort(input_list, start_counter, end_counter))
            start_counter = end_counter+1
            end_counter = start_counter + 4
        # last group incase of non multiples of 5
        if start_counter <= end_index:
            c.append(self.__insertion_sort(input_list, start_counter, end_index))
        return c
