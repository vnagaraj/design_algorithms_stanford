__author__ = 'VGN'

"""File comprising the Graph and its related classes"""


class Edge:
    """Edge class storing the forward vertex of type integer and tail vertex of type integer"""

    def __init__(self, first_vertex, second_vertex, weight=1):
        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.weight = weight # used in Djikstra's shortest path algorithm

    def __eq__(self, other):
        if self.first_vertex == other.first_vertex and self.second_vertex == other.second_vertex:
            return True
        if self.first_vertex == other.second_vertex and self.second_vertex == other.first_vertex:
            return True
        return False

    def __repr__(self):
        return "{} -> {}".format(self.first_vertex, self.second_vertex)

    def __hash__(self):
        return hash(self.first_vertex) * hash(self.second_vertex)


class Graph:
    """Graph class storing the vertex and edges using adjacency list representation"""

    def __init__(self, file_name):
        # list of vertices, index of the list maps to the vertex, with the edge list stored
        # eg: vertex 1 maps to vertex_list[1] which stores the list of edges incident to that vertex
        self.vertex_list = list()
        self.vertex_list.append(list())  # index at 0 is not used, points to an empty list,
        # unique edge set
        self.edge_set = set()
        self._construct_graph(file_name)

    def _construct_graph(self, file_name):
        """Private helper which creates a graph from the given file name
           used for creating graph from pa*.txt """
        with open(file_name, "r") as ins:
            edge_count = 0
            for line in ins:
                line = line.split()
                index = int(line[0])
                edge_list = list()
                for i in range(1, len(line)):
                    end_index = int(line[i])
                    e = Edge(index, end_index)
                    edge_count += 1
                    edge_list.append(e)
                    self.edge_set.add(e)
                self.vertex_list.append(edge_list)


class DirectedGraph:
    """Directed graph using adjacency list representation
        Data structure used by the Kasaraju scc algorithm/ Djikrsta shortest path algorithm
    """

    def __init__(self, file_name, is_scc=True):
        self.vertex_list = list()
        if is_scc:
            # list of vertices, index of the list maps to the vertex, with the [outgoing_edge_list, incoming_edge_list] stored
            self._construct_graph(file_name)
        else:
            # used by Djikstra's algorithm
            # list of vertices, index of list maps to the vertex, with the [outgoing_edge_list]
            self.edge_list = list()
            self._construct_graph_djikstra(file_name)

    def _construct_graph(self, file_name):
        """Private helper which creates a graph from the given file name
           Used for creating directed graph from scc*.txt"""
        with open(file_name, "r") as ins:
            for line in ins:
                line = line.split()
                index = int(line[0])
                if (len(self.vertex_list) < index+1):
                    while len(self.vertex_list) != index + 1:
                        self.vertex_list.append([list(), list()])
                for i in range(1, len(line)):
                    end_index = int(line[i])
                    if (len(self.vertex_list) < end_index+1):
                        while len(self.vertex_list) != end_index + 1:
                            self.vertex_list.append([list(), list()])
                    forward_edge = Edge(index, end_index)
                    backward_edge = Edge(end_index, index)
                    self.vertex_list[index][0].append(forward_edge)
                    self.vertex_list[end_index][1].append(backward_edge)

    def _construct_graph_djikstra(self, file_name):
        """Private helper which creates a graph from the given file name
           Used for creating directed graph from djikstra_*.txt"""
        with open(file_name, "r") as ins:
            for line in ins:
                line = line.split()
                index = int(line[0])
                if (len(self.vertex_list) < index+1):
                    while len(self.vertex_list) != index + 1:
                        self.vertex_list.append(list())
                for i in range(1, len(line)):
                    line_list = line[i].split(",")
                    end_index = int(line_list[0])
                    edge_weight = int(line_list[1])
                    if (len(self.vertex_list) < end_index+1):
                        while len(self.vertex_list) != end_index + 1:
                            self.vertex_list.append(list())
                    edge = Edge(index, end_index, edge_weight)
                    self.vertex_list[index].append(edge)
                    self.edge_list.append(edge)

