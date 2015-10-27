__author__ = 'VGN'

import unittest
import time
import sys
from graph import DirectedGraph
from graph_search import DFS


class SCC:
    """Kosaraju 2 pass alogrithm to compute scc in directed graph"""
    def __init__(self, directed_graph):
        self.directed_graph = directed_graph
        self.finishing_time_list = list()
        self.finishing_time_list.append(-1)
        self.t = 0  # for finishing time in 1st pass
        self.strong_component_size_list = list()
        self.max_size_list= [0, 0, 0, 0, 0]

    def run(self):
        # 1st pass on reverse graph
        self.dfs_loop(self.directed_graph.vertex_list, "reverse", self.t, self.finishing_time_list)
        # 2nd pass on forward graph iterating through finishing time list
        self.dfs_loop(self.finishing_time_list, "not_reverse", None, None, True)

    def dfs_loop(self, loop_list, is_reverse, finishing_time=None, finishing_time_list=None,
                 compute_strong_component=False):
        self.explored_list = list()
        for i in range(0, len(loop_list)):
            self.explored_list.append(False)
        for i in range(len(loop_list)-1, 0, -1):
            if is_reverse == "not_reverse":
                i = int(loop_list[i])
            if not self.explored_list[i]:
                if compute_strong_component:
                    leader = i
                    strong_component_size = 0
                else:
                    strong_component_size = None
                dfs = DFS(i, self.directed_graph, self.explored_list, None, None, None, finishing_time_list, is_reverse, strong_component_size)
                dfs.run()
                # iterative version does not complete on large inputs
                #dfs.run_as_stack()
                if compute_strong_component:
                    self.strong_component_size_list.append(dfs.strong_component_size)
                    if self.max_size_list[4] < dfs.strong_component_size:
                        self.max_size_list[4] = dfs.strong_component_size
                        self.max_size_list = sorted(self.max_size_list, reverse=True)


class StrongConnectedComponentTest(unittest.TestCase):
    """Test class for verifying scc algorithm"""

    def get_size_list(self, file_name):
        sys.setrecursionlimit(10**6)
        g = DirectedGraph(file_name)
        scc = SCC(g)
        scc.run()
        return scc.max_size_list

    def test_scc1(self):
        self.assertTrue(self.get_size_list("scc1.txt") == [3, 3, 3, 0, 0])

    def test_scc2(self):
        self.assertTrue(self.get_size_list("scc2.txt") == [3, 3, 2, 0, 0])

    def test_scc3(self):
        self.assertTrue(self.get_size_list("scc3.txt") == [3, 3, 1, 1, 0])

    def test_scc4(self):
        self.assertTrue(self.get_size_list("scc4.txt") == [7, 1, 0, 0, 0])

    def test_scc5(self):
        self.assertTrue(self.get_size_list("scc5.txt") == [6, 3, 2, 1, 0])

    def test_scc6(self):
        self.assertTrue(self.get_size_list("scc6.txt") == [3, 2, 2, 1, 0])

    def test_scc7(self):
        start_time = time.time()
        size_list = self.get_size_list("SCC.txt")
        print "Duration {}".format(time.time() - start_time)
        self.assertTrue(size_list == [434821, 968, 459, 313, 211])


if __name__ == '__main__':
    unittest.main()

