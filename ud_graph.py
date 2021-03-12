# Course: CS 261
# Author: Philip Beck
# Assignment: 6
# Description: Implements graph ADT using Python dictionaries

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list.keys():
            return
        else:
            self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return
        elif u not in self.adj_list.keys() and v not in self.adj_list.keys():
            self.adj_list[u] = [v]
            self.adj_list[v] = [u]
        elif u in self.adj_list.keys() and v not in self.adj_list.keys():
            self.adj_list[u].append(v)
            self.adj_list[v] = [u]
        elif u not in self.adj_list.keys() and v in self.adj_list.keys():
            self.adj_list[u] = [v]
            self.adj_list[v].append(u)
        else:
            if u in self.adj_list[v] or v in self.adj_list[u]:
                return
            else:
                self.adj_list[u].append(v)
                self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if u not in self.adj_list.keys() or v not in self.adj_list.keys():
            return
        elif u not in self.adj_list[v] or v not in self.adj_list[u]:
            return
        else:
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v not in self.adj_list.keys():
            return
        #remove vertex from neighbors
        for vertex in self.adj_list[v]:
            self.adj_list[vertex].remove(v)
        #remove vertex from list
        self.adj_list.pop(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vertices = []
        for key in self.adj_list.keys():
            vertices.append(key)
        return vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges = []
        edge_dict = self.adj_list.copy()

        #visit every vertex
        for key in edge_dict.keys():
            #ignore unconnected vertices
            if edge_dict[key] != []:
                #build edge tuple, remove duplicates
                for neighbor in edge_dict[key]:
                    edges.append((key, neighbor))
                    edge_dict[neighbor].remove(key)
        
        #dereference copy
        edge_dict = None

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if path == []:
            return True

        #travel entire path
        for i in range(len(path)):
            #catch invalid vertices
            if path[i] not in self.adj_list.keys():
                return False
            #successful path
            elif i == (len(path) - 1):
                return True
            #next vertex is not adjacent
            elif path[i + 1] not in self.adj_list[path[i]]:
                return False

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list.keys():
            return []
        
        if v_end not in self.adj_list.keys():
            v_end = None

        reachable = []
        stack = [v_start]
        
        while stack != []:
            v = stack.pop()
            
            if v == v_end:
                reachable.append(v)
                return reachable

            #travel to next vertex in alphabetical order
            if v not in reachable:
                reachable.append(v)
                for neighbor in sorted(self.adj_list[v], reverse=True):
                    stack.append(neighbor)
        
        return reachable
                
    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list.keys():
            return []
        
        if v_end not in self.adj_list.keys():
            v_end = None

        reachable = []
        queue = [v_start]
    
        while queue != []:
            v = queue.pop(0)

            if v == v_end:
                reachable.append(v)
                return reachable

            if v not in reachable:
                reachable.append(v)
                for neighbor in sorted(self.adj_list[v]):
                    if neighbor not in reachable:
                        queue.append(neighbor)

        return reachable

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        complete = sorted(self.adj_list.keys())
        v = complete[0]
        total_comps = []
        quantity = 0

        while total_comps != complete:
            quantity += 1
            total_comps.extend(self.bfs(v))

            #complete list of vertices are already sorted
            if sorted(total_comps) == complete:
                return quantity

            #cast to sets and find disconnected component
            else:
                v = list(set(complete).difference(set(total_comps)))[0]

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        Uses DFS while checking for back edges
        """
        vertices = list(self.adj_list.keys())
        
        for root in vertices:
            home = set()
            stack = [root]
            while stack != []:
                v = stack.pop()
                home.add(v)


    """
                if self.adj_list[v] != []:
                    for adjacent in self.adj_list[v]:
                        for neighbor in self.adj_list[adjacent]:
                            if not set(self.adj_list[neighbor]).isdisjoint(home):
                                return True
                        queue.append(adjacent)
            
        return False
    """

   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle(), g)
