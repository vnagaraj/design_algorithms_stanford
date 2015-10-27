__author__ = 'VGN'

import unittest
from graph import Graph


class GenericSearch(object):
    """Generic search class overridden by specific subclasses"""

    def __init__(self, source_vertex, graph, explored_list=None, component_identifier_dict=None):
        self.source_vertex = source_vertex
        self.graph = graph
        # boolean list to keep track of explored vertices
        if not explored_list:
            self.explored_list = list()
            for vertex in self.graph.vertex_list:
                self.explored_list.append(False)
        else:
            self.explored_list = explored_list
        self.component_identifier_dict = component_identifier_dict

    def run(self):
        pass


class BFS(GenericSearch):
    """class to compute the breadth first search starting from a given vertex"""

    def __init__(self, source_vertex, graph, explored_list=None, component_identifier_dict=None):
        super(BFS, self).__init__(source_vertex, graph, explored_list, component_identifier_dict)
        #to compute shortest path from a given vertex(special property of BFS)
        self.dist_list = list()
        for vertex in self.graph.vertex_list:
            self.dist_list.append(-1)

    def run(self):
        queue = Queue()
        queue.enqueue(self.source_vertex)
        self.explored_list[self.source_vertex] = True
        self.dist_list[self.source_vertex] = 0
        self.component_identifier_dict[self.source_vertex] = self.source_vertex
        while not queue.is_empty():
            vertex = queue.deque()
            edge_list = self.graph.vertex_list[vertex]
            for edge in edge_list:
                if not self.explored_list[edge.second_vertex]:
                    queue.enqueue(edge.second_vertex)
                    self.explored_list[edge.second_vertex] = True
                    self.dist_list[edge.second_vertex] = self.dist_list[edge.first_vertex] + 1
                    # needed in case for computing connected components
                    if self.component_identifier_dict:
                        self.component_identifier_dict[edge.second_vertex] = self.source_vertex


class DFS(GenericSearch):
    """class to compute the depth first search starting from a given vertex"""

    def __init__(self, source_vertex, graph, explored_list=None, component_identifier_dict=None, current_label=None, top_ordering_list=None,
                 finishing_time_list=None, reverse_graph=None, strong_component_size=None):
        super(DFS, self).__init__(source_vertex, graph, explored_list, component_identifier_dict)
        # required for topological ordering
        self.current_label = current_label
        self.top_ordering_list = top_ordering_list
        # required for computing strong components
        self.finishing_time_list = finishing_time_list
        self.reverse_graph = reverse_graph
        self.strong_component_size = strong_component_size

    def run(self):
        self._recursive_dfs(self.source_vertex)

    def run_as_stack(self):
        self._run_using_explicit_stack_dfs(self.source_vertex)

    def _recursive_dfs(self, vertex):
        self.explored_list[vertex] = True
        if self.component_identifier_dict:
            self.component_identifier_dict[vertex] = self.source_vertex
        if self.reverse_graph is not None:
            if self.reverse_graph == "reverse":
                edge_list = self.graph.vertex_list[vertex][1]
            else:
                edge_list = self.graph.vertex_list[vertex][0]
        else:
            edge_list = self.graph.vertex_list[vertex]
        for edge in edge_list:
            if not self.explored_list[edge.second_vertex]:
                self._recursive_dfs(edge.second_vertex)
        if self.top_ordering_list is not None and self.current_label is not None:
            self.top_ordering_list[self.current_label] = vertex
            self.current_label -= 1
        if self.finishing_time_list is not None:
            self.finishing_time_list.append(vertex)
        if self.strong_component_size is not None:
            self.strong_component_size += 1

    def _run_using_explicit_stack_dfs(self, vertex):
      #stack = Stack()
      stack = list()
      #stack.push(vertex)
      stack.append(vertex)
      pop_list = list()
      for i in range(0, len(self.explored_list)):
          pop_list.append(False)
      #while not stack.is_empty():
      while len(stack) != 0:
          #vertex = stack.peek()
          vertex = stack[len(stack)-1]
          if self.explored_list[vertex]:
              vertex = stack.pop()
              if not pop_list[vertex]:
                  pop_list[vertex] = True
                  if self.strong_component_size is not None:
                    self.strong_component_size+= 1
                  if self.finishing_time_list is not None:
                        self.finishing_time_list.append(vertex)
          else:
            if self.reverse_graph is not None:
                if self.reverse_graph == "reverse":
                    edge_list = self.graph.vertex_list[vertex][1]
                else:
                    edge_list = self.graph.vertex_list[vertex][0]
            else:
                edge_list = self.graph.vertex_list[vertex]
            for edge in edge_list:
                if not self.explored_list[edge.second_vertex]:
                    #stack.push(edge.second_vertex)
                    stack.append(edge.second_vertex)
            self.explored_list[vertex] = True


class ConnectedComponents:
    """class to compute connected components of graph using BFS/DFS"""

    def __init__(self, graph, use_bfs=True):
        self.graph = graph
        self.explored_list = list()
        self.component_identifier_dict = {}
        self.init_explored_list()
        self.is_bfs = use_bfs

    def init_explored_list(self):
        for vertex in range(0, len(self.graph.vertex_list)):
            self.explored_list.append(False)
            if vertex != 0:
                self.component_identifier_dict[vertex] = vertex

    def run(self):
        for vertex in range(1, len(self.graph.vertex_list)):
            if not self.explored_list[vertex]:
                if self.is_bfs:
                    bfs = BFS(vertex, self.graph, self.explored_list, self.component_identifier_dict)
                    bfs.run()
                else:
                    # use DFS for computing connected components
                    dfs = DFS(vertex, self.graph, self.explored_list, self.component_identifier_dict)
                    #dfs.run()
                    dfs.run_using_explicit_stack_dfs()


    def compute_connected_components(self):
        """return dictionary with key as component_id as value : list of vertices belonging to that component"""
        connected_comp_dict = {}
        for key in self.component_identifier_dict:
            if self.component_identifier_dict[key] not in connected_comp_dict:
                connected_comp_dict[self.component_identifier_dict[key]] = [key]
            else:
                connected_comp_dict[self.component_identifier_dict[key]].append(key)
        return connected_comp_dict


class TopologicalOrdering:
    """Class to compute topological ordering of a directed graph using dfs"""
    def __init__(self, graph):
        self.graph = graph
        self.explored_list = list() # to keep track of explored vertices
        self._top_ordering_list = list() # to keep track of top ordering, index of this list points to the finishing time of vertex
        for vertex in self.graph.vertex_list:
            self.explored_list.append(False)
            self._top_ordering_list.append(-1)
        self.current_label = len(self.graph.vertex_list)-1

    def run(self):
        for vertex in range(1, len(self.graph.vertex_list)):
            if not self.explored_list[vertex]:
                dfs = DFS(vertex, self.graph, self.explored_list, None, self.current_label, self._top_ordering_list)
                dfs.run()
                #dfs.run_using_explicit_stack_dfs()

    def print_top_ordering(self):
        for vertex in range(1, len(self._top_ordering_list)):
            if vertex == len(self._top_ordering_list)-1:
                print "Vertex {}".format(self._top_ordering_list[vertex])
            else:
                print "Vertex {} ->".format(self._top_ordering_list[vertex]),


class Queue:
    """ queue data structure implemented using a single link list to support enqueue from front and dequeue from back
    """

    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0

    def enqueue(self, val):
        self.size += 1
        if not self.first:
            self.first = Node(val)
            if not self.last:  # case when size=1
                self.last = self.first
                return
        temp = self.last
        self.last = Node(val)
        temp.next = self.last

    def deque(self):
        if not self.first:
            raise Exception("Cannot remove from empty queue")
        node = self.first
        self.first = self.first.next
        if self.first is None:
            self.last = None
        self.size -= 1
        return node.val

    def is_empty(self):
        return self.first is None


class Stack:
    """ stack data structure implemented using a single link list to support push/pop from front of the list
    """

    def __init__(self):
        self.first = None
        self.size = 0

    def push(self, val):
        self.size += 1
        temp = self.first
        self.first = Node(val)
        self.first.next = temp

    def pop(self):
        if not self.first:
            raise Exception("Cannot remove from empty queue")
        node = self.first
        self.first = self.first.next
        self.size -= 1
        return node.val

    def peek(self):
        if not self.first:
            raise Exception("Cannot peek from empty queue")
        return self.first.val

    def is_empty(self):
        return self.first is None


class Node:
    """Internal class for implementing queue"""

    def __init__(self, val):
        self.val = val
        self.next = None


class ConnectedComponentTest(unittest.TestCase):
    def test_bfs1(self):
        g = Graph("search.txt")
        connected_components = ConnectedComponents(g)
        connected_components.run()
        print "BFS connected components {} ".format(connected_components.compute_connected_components())
        # use DFS
        connected_components = ConnectedComponents(g, False)
        connected_components.run()
        print "DFS connected components {} ".format(connected_components.compute_connected_components())
        # top ordering using DFS
        g = Graph("top_ordering.txt")
        top_ordering = TopologicalOrdering(g)
        top_ordering.run()
        top_ordering.print_top_ordering()
        # using explicit stack DFS

if __name__ == '__main__':
    unittest.main()