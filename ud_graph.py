# Author: Philip Beck
# Email: stoneroll6@gmail.com
# Date: 1/17/2021
# Description:
#    Implements undirected graph ADT 
#    using Python dictionaries
#    For educational use only,
#    Not for commercial use


class UndirectedGraph:
    """
    Class to implement undirected graph
    - Duplicate edges not allowed
    - Loops not allowed
    - No edge weights
    - Vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        """
        self.adj_list = dict()

        # Populate graph with initial vertices and edges (if provided)
        # Before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

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
        # Remove vertex from neighbors
        for vertex in self.adj_list[v]:
            self.adj_list[vertex].remove(v)
        # Remove vertex from list
        self.adj_list.pop(v)

    def get_vertices(self) -> list:
        """
        Return list of vertices in the graph (any order)
        """
        vertices = []
        for key in self.adj_list.keys():
            vertices.append(key)
        return vertices

    def get_edges(self) -> list:
        """
        Return list of edges in the graph (any order)
        """
        edges = []
        edge_dict = self.adj_list.copy()

        # Visit every vertex
        for key in edge_dict.keys():
            # Ignore unconnected vertices
            if edge_dict[key] != []:
                # Build edge tuple, remove duplicates
                for neighbor in edge_dict[key]:
                    edges.append((key, neighbor))
                    edge_dict[neighbor].remove(key)
        
        # Dereference copy
        edge_dict = None

        return edges

    def is_valid_path(self, path: list) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if path == []:
            return True

        # Travel entire path
        for i in range(len(path)):
            # Catch invalid vertices
            if path[i] not in self.adj_list.keys():
                return False
            # Successful path
            elif i == (len(path) - 1):
                return True
            # Next vertex is not adjacent
            elif path[i + 1] not in self.adj_list[path[i]]:
                return False

    def dfs(self, v_start, v_end=None) -> list:
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

            # Travel to next vertex in alphabetical order
            if v not in reachable:
                reachable.append(v)
                for neighbor in sorted(self.adj_list[v], reverse=True):
                    stack.append(neighbor)
        
        return reachable
                
    def bfs(self, v_start, v_end=None) -> list:
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

    def count_connected_components(self) -> int:
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

            # Complete list of vertices are already sorted
            if sorted(total_comps) == complete:
                return quantity

            # Cast to sets and find disconnected component
            else:
                v = list(set(complete).difference(set(total_comps)))[0]

    def has_cycle(self) -> bool:
        """
        Return True if graph contains a cycle, False otherwise
        """
        # Check multiple connected components
        for i in list(self.adj_list.keys()):
            # Initialize visited list with root
            visited = [i]
            # Initialize stack with 2nd-degree neighbors
            for adjacent in self.adj_list[i]:
                stack = []
                for neighbor in self.adj_list[adjacent]:
                    if neighbor != i:
                        stack.append(neighbor)
                result = self.has_cycle_helper(adjacent, visited, stack)
                if result is True:
                    return True
        return False

    def has_cycle_helper(self, vertex, visited: list, stack: list) -> bool:
        while stack != []:
            v = stack.pop()
            # Check 2nd-degree neighbors for any backedge
            if not set(self.adj_list[v]).isdisjoint(set(visited)):
                return True
            # Pass down new lists to next recursive level
            else:
                new_visited = visited.copy()
                new_visited.append(vertex)
                new_stack = []
                for adjacent in self.adj_list[v]:
                    if adjacent != vertex:
                        new_stack.append(adjacent)
                result = self.has_cycle_helper(v, new_visited, new_stack)
                if result is True:
                    return True
        return False


if __name__ == '__main__':

    # Examples to show graph functionality
    # Adds vertex or edge to graph
    print("\nmethod add_vertex() / add_edge example 1")
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

    # Removes vertex or edge from graph
    print("\nmethod remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    # Gets vertices or edges from graph
    print("\nmethod get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    # Checks valid path in graph
    print("\nmethod is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    # Uses DFS or BFS in graph to find element
    print("\nmethod dfs() and bfs() example 1")
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

    # Returns number of connected components
    print("\nmethod count_connected_components() example 1")
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

    # Checks if graph has cycle
    print("\nmethod has_cycle() example 1")
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
        print('{:<10}'.format(case), g.has_cycle())
