__author__ = 'VGN'

import unittest
import math
import random
import time
from graph import Graph


class RandomContraction:
    """Class to compute the min cut of the graph"""
    def __init__(self, graph):
        self.graph = graph
        self.init_root()

    def init_root(self):
        self.root_list = list()  # list for identifying the root/parent of the vertex
        self.root_dict = {}  # dict for keeping track of connected components, key as root, value as members
        self.root_list.append(0)
        for i in range(1, len(self.graph.vertex_list)):
            self.root_list.append(i)
            self.root_dict[i] = [i]

    def get_root(self, vertex):
        val = self.root_list[vertex]
        while val != vertex:
            vertex = val
            val = self.root_list[vertex]
        return val

    def fuse_vertices(self, vertex1, vertex2):
        root1 = self.get_root(vertex1)
        root2 = self.get_root(vertex2)
        if root1 != root2:
            self.root_list[root1] = root2
            self.root_dict[root2] += self.root_dict[root1]
            del self.root_dict[root1]

    def run(self, no_trials=None):
        # no of trials = n*n* logn
        edge_set = set(self.graph.edge_set)
        no_vertices = len(self.graph.vertex_list)-1
        if no_trials is None:
            no_trials = int(no_vertices * no_vertices * math.log(no_vertices, 2))
        #print "no_trials {}".format(no_trials)
        else:
            no_trials = 100
        n = no_vertices
        min_cut = -1
        for i in range(0, no_trials):
            start_time = time.time()
            while n > 2:
                #pick an edge uniformly at random from the edge set
                edge = random.choice(list(edge_set))
                #edge = list(edge_set)[1]
                first_vertex = edge.first_vertex
                second_vertex = edge.second_vertex
                # fuse first_vertex and second_vertex
                self.fuse_vertices(first_vertex, second_vertex)
                # delete edge from edge set
                edge_set.remove(edge)
                self.delete_self_loops(first_vertex, edge_set)
                n = n - 1
            current_cut = len(edge_set)
            if min_cut == -1:
                min_cut = current_cut
            elif current_cut < min_cut:
                min_cut = current_cut

            # reset data structures for next trial
            edge_set = set(self.graph.edge_set)
            n = no_vertices
            self.init_root()

        return min_cut

    def delete_self_loops(self, vertex, edge_set):
        graph_vertex_list = self.graph.vertex_list
        # check for self loops only for the fused vertices(belonging to same component)
        root = self.get_root(vertex)
        root_vertex_list = self.root_dict[root]
        for vertex in root_vertex_list:
            for e in graph_vertex_list[vertex]:
                # check for self loops
                if self.get_root(e.first_vertex) == self.get_root(e.second_vertex):
                    if e in edge_set:
                        edge_set.remove(e)


class RandomContractionTest(unittest.TestCase):

    def test_pa1(self):
        g = Graph("pa1.txt")
        random_contraction = RandomContraction(g)
        min_cut = random_contraction.run()
        print min_cut
        self.assertTrue(min_cut == 2)

    def test_pa2(self):
        g = Graph("pa2.txt")
        random_contraction = RandomContraction(g)
        min_cut = random_contraction.run()
        print min_cut
        self.assertTrue(min_cut == 2)

    def test_pa3(self):
        g = Graph("pa3.txt")
        random_contraction = RandomContraction(g)
        min_cut = random_contraction.run()
        self.assertTrue(min_cut == 1)

    def test_pa4(self):
        g = Graph("pa4.txt")
        random_contraction = RandomContraction(g)
        min_cut = random_contraction.run()
        self.assertTrue(min_cut == 2)

    def test_pa5(self):
        g = Graph("pa5.txt")
        random_contraction = RandomContraction(g)
        min_cut = random_contraction.run()
        self.assertTrue(min_cut == 3)

    def test_pa6(self):
        g = Graph("pa6.txt")
        random_contraction = RandomContraction(g)
        min_cut = random_contraction.run()
        self.assertTrue(min_cut == 9)

    def test_karger_min_cut(self):
        g = Graph("kargerMinCut.txt")
        random_contraction = RandomContraction(g)
        start_time = time.time()
        min_cut = random_contraction.run(100)
        end_time = time.time()
        self.assertTrue(min_cut == 17)
        print "Time take {}".format(end_time - start_time)


if __name__ == '__main__':
    unittest.main()