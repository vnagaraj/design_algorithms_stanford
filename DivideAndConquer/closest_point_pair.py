__author__ = 'VGN'

import math
import sys
import unittest
import random


class NotPointClassException(Exception):
    def __init__(self, message):
        self.message = message


def compare_y(p):
    """Custom comparator point class to compare by y co-ordinate"""
    return p.y


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        if self.__attrs() == other.__attrs():
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __attrs(self):
        return self.x, self.y

    def __repr__(self):
        return "X = {}, Y = {}".format(str(self.x), str(self.y))

    def distance_to(self, other):
        """compute the euclidean distance between self and other"""
        return math.sqrt(math.pow(self.x-other.x, 2) + math.pow(self.y - other.y, 2))

    def __hash__(self):
        return hash(self.__attrs())

    def __lt__(self, other):
        """
        Default comparator done on x axis
        """
        if not isinstance(other, Point):
            raise NotPointClassException("Comparison of not type Point")
        if self.x < other.x:
            return True
        return False


class ClosestPointPair:

    def __init__(self, point_list):
        self.point_list = point_list

    def closest_pair(self):
        # create separate copies for px and py
        p_x = self.point_list[:]
        p_y = self.point_list[:]
        # sort p_x by x_co-ordinate
        p_x.sort()
        # sort p_y by y_co-ordinate
        p_y.sort(key=compare_y)
        start_index = 0
        end_index = len(self.point_list) -1
        return self._recursive_closest_pair(p_x, p_y, start_index, end_index)

    def _recursive_closest_pair(self, p_x, p_y, start_index, end_index):
        if end_index - start_index <= 3:# base case
            return self._compute_closest_pair_brute_force(p_x, start_index, end_index)
        middle_index = (end_index - start_index)/2 + start_index
        left_closest_pair = self._recursive_closest_pair(p_x, p_y, start_index, middle_index)
        right_closest_pair = self._recursive_closest_pair(p_x, p_y, middle_index+1, end_index)
        delta = self._get_min_dist(left_closest_pair, right_closest_pair)
        split_closest_pair = self.closest_split_pair(p_x, p_y, middle_index, delta)
        if split_closest_pair is None:
            return self._get_min_pair(left_closest_pair, right_closest_pair)
        else:
            return split_closest_pair

    def _get_min_pair(self, pair1, pair2):
        dist1 = pair1[0].distance_to(pair1[1])
        dist2 = pair2[0].distance_to(pair2[1])
        if dist1 < dist2:
            return pair1
        else:
            return pair2

    def _get_min_dist(self, pair1, pair2):
        dist1 = pair1[0].distance_to(pair1[1])
        dist2 = pair2[0].distance_to(pair2[1])
        if dist1 < dist2:
            return dist1
        else:
            return dist2

    def closest_split_pair(self, p_x, p_y, middle_index, delta):
        x_bar = p_x[middle_index].x
        # create s_y from p_y based on points having x_coordinate range in [xbar- delata, xbar+delta]
        s_y = list()
        lower_range = x_bar- delta
        upper_range = x_bar + delta
        for i in range(len(p_y)):
            if (lower_range <= p_y[i].x <= upper_range):
                s_y.append(p_y[i])
        best = delta
        best_pair = None
        length = len(s_y)
        for i in range(length):
            for j in range(1, min(7, length-i)):
                p = s_y[i]
                q = s_y[i+j]
                dist = p.distance_to(q)
                if dist < best:
                    best = dist
                    best_pair = (p, q)
        return best_pair

    def closest_pair_brute_force(self):
        return self._compute_closest_pair_brute_force(self.point_list, 0, len(self.point_list)-1)

    def _compute_closest_pair_brute_force(self, p_list, start_index, end_index):
        closest_pair = None
        min_distance = sys.maxint
        for i in range(start_index, end_index+1):
            for j in range(i+1, end_index+1):
                p = p_list[i]
                q = p_list[j]
                dist = p.distance_to(q)
                if dist < min_distance:
                    min_distance = dist
                    closest_pair = (p, q)
        return closest_pair


class TestClosestPointPair(unittest.TestCase):

        def _test(self, n):
            point_list = self._build_random_point_list(n)
            print "point_list {}".format(point_list)
            closest_point_pair = ClosestPointPair(point_list)
            val1 = closest_point_pair.closest_pair_brute_force()
            dist_bruteforce = val1[0].distance_to(val1[1])
            val2 = closest_point_pair.closest_pair()
            print "val_bruteforce {}".format(val1)
            print "val_divideconquer {}".format(val2)
            dist_divideconquer = val2[0].distance_to(val2[1])
            print "dist_bruteforce {}".format(dist_bruteforce)
            print "dist_divideconquer {}".format(dist_divideconquer)
            self.assertTrue(dist_bruteforce == dist_divideconquer)

        def test_20x20(self):
            self._test(20)

        def _build_random_point_list(self, n):
            z = set()
            for i in range(n):
                z.add(Point(random.randint(1, 100), random.randint(1, 100)))
            return list(z)

if __name__ == '__main__':
    unittest.main()