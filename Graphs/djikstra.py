__author__ = 'VGN'

import sys
import time
import unittest
from graph import DirectedGraph
from heap import MinHeap


class Key:
    """ key class to be used by Djikstra's to place this object in heap,
        keys are compared based on distance attribute(distance of the vertex from source vertex)
    """

    def __init__(self, vertex):
        self.vertex = vertex
        self.distance = sys.maxint

    def __lt__(self, other):
        """
        Default comparator done on key attribute
        """
        if not isinstance(other, Key):
            raise Exception("Comparison of not type Key")
        if self.distance < other.distance:
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, Key):
            return False
        if self.vertex == other.vertex:
            return True
        return False

    def __repr__(self):
        return "Vertex = {}, Key = {}".format(str(self.vertex), str(self.distance))

    def __hash__(self):
        return hash(self.vertex)


class Djikstra:
    """ class to compute the shortest path from the given vertex using djikstra's algorithm"""

    def __init__(self, source_vertex, graph):
        self.source_vertex = source_vertex
        self.graph = graph
        self.explored_list = list()  # boolean list to keep track if vertices belong to "X"(vertices explored from source vertex)
        for i in range(0, len(graph.vertex_list)):
            self.explored_list.append(False)
        self.dist_list = list()  # distance list to keep track of shortest distance from source vertex to the given vertex
        for i in range(0, len(graph.vertex_list)):
            self.dist_list.append(sys.maxint)

    def run(self):
        # init step
        self.explored_list[self.source_vertex] = True  # marking source belong to "X"(set of explored vertices)
        self.dist_list[self.source_vertex] = 0  # shortest distance from source to itself is 0 ( no negative edges)
        edge_list = self.graph.edge_list
        no_iterations = len(self.graph.vertex_list) - 2  # excluding index 0
        while no_iterations > 0:
            min_score = sys.maxint
            chosen_vertex = None
            for edge in edge_list:
                # check if head of edge is in set "X" and tail of edge is outside of "X"
                if self.explored_list[edge.first_vertex] and not self.explored_list[edge.second_vertex]:
                    djikstra_greedy_score = self.dist_list[edge.first_vertex] + edge.weight
                    if djikstra_greedy_score < min_score:
                        min_score = djikstra_greedy_score
                        chosen_vertex = edge.second_vertex  # vertex to select to place in set "X"
            # set the chosen_vetex to set "X"
            self.explored_list[chosen_vertex] = True
            # set the distance of the chosen vertex
            self.dist_list[chosen_vertex] = min_score
            no_iterations -= 1

    def run_using_heap(self):
        # init step
        min_heap = MinHeap()
        self.explored_list[self.source_vertex] = True  # marking source belong to "X"(set of explored vertices)
        self.dist_list[self.source_vertex] = 0  # shortest distance from source to itself is 0 ( no negative edges)
        edges = self.graph.vertex_list[self.source_vertex]
        for edge in edges:
            key = Key(edge.second_vertex)
            key.distance = edge.weight
            min_heap.insert(key)
        while not min_heap.is_empty():
            key = min_heap.extract_min()
            # set the chosen_vertex to set "X"
            self.explored_list[key.vertex] = True
            # set the distance of the chosen vertex
            self.dist_list[key.vertex] = key.distance
            edge_list = self.graph.vertex_list[key.vertex]
            for edge in edge_list:
                # check if head of edge is in set "X" and tail of edge is outside of "X"
                if self.explored_list[edge.first_vertex] and not self.explored_list[edge.second_vertex]:
                    index = min_heap.get_index_of_element(Key(edge.second_vertex))
                    if index == -1: # element not in heap
                        min_heap.insert(Key(edge.second_vertex))
                        index = min_heap.get_index_of_element(Key(edge.second_vertex))
                    key_second_vertex = min_heap.get_element_from_index(index)
                    # delete Key(vertex) from heap
                    min_heap.delete_at_index(index)
                    # recompute key of vertex
                    djikstra_greedy_score = self.dist_list[edge.first_vertex] + edge.weight
                    if djikstra_greedy_score < key_second_vertex.distance:
                        key_second_vertex.distance = djikstra_greedy_score
                    #insert vertex back to heap
                    min_heap.insert(key_second_vertex)


class DjikstraTest(unittest.TestCase):
    """Test class for verifying scc algorithm"""

    def get_dist_list(self, file_name, start_vertex=1, use_heap=False):
        g = DirectedGraph(file_name, False)
        djikstra = Djikstra(start_vertex, g)
        if not use_heap:
            djikstra.run()
        else:
            djikstra.run_using_heap()
        return djikstra.dist_list

    def test_djikstra1(self):
        self.assertTrue(self.get_dist_list("djikstra_1.txt")[1:] == [0, 3, 3, 5])
        self.assertTrue(self.get_dist_list("djikstra_1.txt", 1, True)[1:] == [0, 3, 3, 5])

    def test_djikstra2(self):
        self.assertTrue(self.get_dist_list("djikstra_2.txt")[1:] == [0, 3, 4, 5])
        self.assertTrue(self.get_dist_list("djikstra_2.txt", 1, True)[1:] == [0, 3, 4, 5])

    def test_djikstra3(self):
        dist_list = self.get_dist_list("djikstra_3.txt")
        self.assertTrue(dist_list[4] == 2)
        dist_list = self.get_dist_list("djikstra_3.txt", 1, True)
        self.assertTrue(dist_list[4] == 2)

    def test_djikstra4(self):
        dist_list = self.get_dist_list("djikstra_4.txt")
        self.assertTrue(dist_list[7] == 5)
        dist_list = self.get_dist_list("djikstra_4.txt", 1, True)
        self.assertTrue(dist_list[7] == 5)

    def test_djikstra5(self):
        dist_list = self.get_dist_list("djikstra_5.txt", 13)
        self.assertTrue(dist_list[5] == 26)
        dist_list = self.get_dist_list("djikstra_5.txt", 13, True)
        self.assertTrue(dist_list[5] == 26)

    def test_djikstra6(self):
        dist_list = self.get_dist_list("djikstra_6.txt")
        output_list = [dist_list[7], dist_list[37], dist_list[59], dist_list[82], dist_list[99], dist_list[115],
                       dist_list[133], dist_list[165], dist_list[188], dist_list[197]]
        self.assertTrue(output_list == [4758, 4132, 3900, 1827, 3700, 3532, 3299, 3062, 1501, 4255])
        dist_list = self.get_dist_list("djikstra_6.txt", 1, True)
        output_list = [dist_list[7], dist_list[37], dist_list[59], dist_list[82], dist_list[99], dist_list[115],
                       dist_list[133], dist_list[165], dist_list[188], dist_list[197]]
        self.assertTrue(output_list == [4758, 4132, 3900, 1827, 3700, 3532, 3299, 3062, 1501, 4255])

    def test_djikstra7(self):
        self.assertTrue(self.get_dist_list("djikstra_7.txt")[1:] == [0, 1, 3, 7])
        self.assertTrue(self.get_dist_list("djikstra_7.txt", 1, True)[1:] == [0, 1, 3, 7])

    def test_djikstra8(self):
        self.assertTrue(self.get_dist_list("djikstra_8.txt")[1:] == [0, 1, 2, 1])
        self.assertTrue(self.get_dist_list("djikstra_8.txt", 1, True)[1:] == [0, 1, 2, 1])

    def test_djikstra9(self):
        self.assertTrue(self.get_dist_list("djikstra_9.txt")[1:] == [0, 1, 3, 6])
        self.assertTrue(self.get_dist_list("djikstra_9.txt", 1, True)[1:] == [0, 1, 3, 6])

    def test_djikstra(self):
        #Homework assignment
        start_time = time.time()
        dist_list = self.get_dist_list("djikstra.txt")
        end_time = time.time()
        print "Duration {}".format(end_time - start_time)
        output_list = [dist_list[7], dist_list[37], dist_list[59], dist_list[82], dist_list[99], dist_list[115],
                       dist_list[133], dist_list[165], dist_list[188], dist_list[197]]
        self.assertTrue(output_list == [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068])
        start_time = time.time()
        dist_list = self.get_dist_list("djikstra.txt", 1, True)
        end_time = time.time()
        print "Duration {}".format(end_time - start_time)
        output_list = [dist_list[7], dist_list[37], dist_list[59], dist_list[82], dist_list[99], dist_list[115],
                       dist_list[133], dist_list[165], dist_list[188], dist_list[197]]
        self.assertTrue(output_list == [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068])


if __name__ == '__main__':
    unittest.main()


