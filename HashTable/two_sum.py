__author__ = 'VGN'

import unittest
import time
from hash_table import ChainingHashTable


class TwoSum:

    lower_bound = -10000
    upper_bound = 10000

    def __init__(self, integer_list, dict_type= "inbuilt_dict"):
        if dict_type == "inbuilt_dict":
            self.two_sum_dict = {}
        elif dict_type == "open_chaining":
            self.two_sum_dict = ChainingHashTable()
        st_time = time.time()
        self.two_sum_dict = self.insert_dict(integer_list, self.two_sum_dict)
        end_time = time.time()
        print "time for insert dictionary {}".format(end_time - st_time)
        st_time = time.time()
        self.targets = self._compute_two_sum()
        print "time for compute {}".format(time.time() - st_time)

    def insert_dict(self, integer_list, new_dict):
        for integer in integer_list:
            if integer/10000 not in new_dict:
                new_dict[integer/10000] = [integer]
            else:
                new_dict[integer/10000].append(integer)
        return new_dict

    def _compute_two_sum(self):
        target_set = set()
        for keyX in self.two_sum_dict:
            key_list = [-keyX - 2, -keyX - 1, -keyX] # buckets in which x+y= target_interval(lowerbound<= target <= upperbound)
            bucketX = self.two_sum_dict[keyX]
            for keyY in key_list:
                if keyY in self.two_sum_dict:
                    bucketY = self.two_sum_dict[keyY]
                    for i in range(0, len(bucketX)):
                        for j in range(0, len(bucketY)):
                            x = bucketX[i]
                            y = bucketY[j]
                            if x != y:
                                if x + y >= TwoSum.lower_bound and x +y <= TwoSum.upper_bound:
                                    target_set.add(x+y)
                                    #target_set[x + y] = (x, y)
        return len(target_set)

    def _compute_two_sum_ct(self):
        target_set = set()
        for keyX in self.two_sum_dict:
            key_list = [-keyX - 2, -keyX - 1, -keyX] # buckets in which x+y= target_interval(lowerbound<= target <= upperbound)
            bucketX = self.two_sum_dict[keyX]
            for keyY in key_list:
                if keyY in self.two_sum_dict:
                    bucketY = self.two_sum_dict[keyY]
                    for i in range(0, len(bucketX)):
                        for j in range(0, len(bucketY)):
                            x = bucketX[i]
                            y = bucketY[j]
                            if x != y:
                                if x + y >= TwoSum.lower_bound and x +y <= TwoSum.upper_bound:
                                    target_set.add(x+y)
                                    #target_set[x + y] = (x, y)
        return target_set


class TwoSumTest(unittest.TestCase):
    """Test class for verifying heap data structure"""

    def create_list(self, file_name):
        new_list = list()
        with open(file_name, "r") as ins:
            for line in ins:
                new_list.append(int(line))
        return new_list

    def test1(self):
        print "Results Test1"
        start_time = time.time()
        integer_list = self.create_list("two_sum1.txt")
        print "time for insert into list {}".format(time.time() - start_time)
        start_time = time.time()
        self.assertTrue(TwoSum(integer_list).targets == 121)
        print "Duration using inbuilt dict {}".format(time.time() - start_time)
        start_time = time.time()
        self.assertTrue(TwoSum(integer_list, "open_chaining").targets == 121)
        print "Duration using Openchaining dict {}".format(time.time() - start_time)

    def test2(self):
        print "Results Test2"
        start_time = time.time()
        integer_list = self.create_list("two_sum.txt")
        print "time for insert into list {}".format(time.time() - start_time)
        start_time = time.time()
        self.assertTrue(TwoSum(integer_list).targets) == 427
        print "Duration using inbuilt dict {}".format(time.time() - start_time)


if __name__ == '__main__':
    unittest.main()


