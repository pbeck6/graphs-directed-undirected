# Course: CS261 - Data Structures
# Author: Philip Beck
# Assignment: 6
# Description: Implements directed graph ADT using Python dictionaries

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds vertex, returns # of vertices
        """
        self.adj_matrix.append([0]) 
        self.v_count += 1

        #update number of columns in each row
        for _ in range(self.v_count - 1):
            self.adj_matrix[self.v_count - 1].append(0)
        for i in range(self.v_count - 1):
            self.adj_matrix[i].append(0)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds/updates weighted edge between two vertices
        """
        if src >= self.v_count or dst >= self.v_count \
            or weight < 1 or src == dst or src < 0 or dst < 0:
            return
    
        else:
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes directed edge between two vertices
        """
        if src >= self.v_count or dst >= self.v_count \
            or src < 0 or dst < 0:
            return

        else:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of vertices
        """
        vertices = []
        for i in range(self.v_count):
            vertices.append(i)
        return vertices

    def get_edges(self) -> []:
        """
        Returns list of edges as tuples -> (src,dst,weight)
        """
        edges = []
        for i in range(self.v_count):
            for j in range(self.v_count):
                if self.adj_matrix[i][j] > 0:
                    edges.append((i, j, self.adj_matrix[i][j]))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Determines if list of index vertices is valid path
        """
        if len(path) > 1:
            for i in range(len(path) - 1):
                if self.adj_matrix[path[i]][path[i+1]] == 0:
                    return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Performs depth-first search and returns list
        of visited vertices in order of visit
        """
        visited = []

        #catch invalid indices
        if v_start < 0 or v_start >= len(self.adj_matrix):
            return visited
        elif v_end is not None:
            if v_end < 0 or v_end >= len(self.adj_matrix):
                v_end = None

        #stack goes as deep as possible, then back-tracks
        else:
            stack = [v_start]
            while stack:
                index = stack.pop()
                if index not in visited:
                    visited.append(index)
                v = self.adj_matrix[index]
                #check vertices in ascending order
                for i in range(len(v) - 1, -1, -1):
                    if v[i] > 0 and i not in visited:
                        stack.append(i)
                    if i == v_end:
                        visited.append(i)
                        return visited
            return visited            

    def bfs(self, v_start, v_end=None) -> []:
        """
        Performs breadth-first search and returns list
        of visited vertices in order of visit
        """
        visited = []

        #catch invalid indices
        if v_start < 0 or v_start >= len(self.adj_matrix):
            return visited
        elif v_end is not None:
            if v_end < 0 or v_end >= len(self.adj_matrix):
                v_end = None

        else:
            queue = [v_start]
            while queue:
                index = queue.pop(0)
                if index not in visited:
                    visited.append(index)
                v = self.adj_matrix[index]
                #check vertices in ascending order
                for i in range(self.v_count):
                    if v[i] > 0 and i not in visited:
                        queue.append(i)
                    if i == v_end:
                        visited.append(i)
                        return visited
            return visited

    def has_cycle(self) -> bool:
        """
        Determines if graph has at least one cycle
        """
        pass

    def dijkstra(self, src: int) -> []:
        """
        TODO: Write this implementation
        """
        pass


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
