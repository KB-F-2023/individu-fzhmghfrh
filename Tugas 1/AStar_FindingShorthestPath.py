from queue import PriorityQueue
# PriorityQueue data structure is used to Keep track
# of the nodes to explore next based on
# their estimated total cost (new_cost + heuristic).

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.costs = {}
        self.heuristics = {}

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = []
        if node not in self.costs:
            self.costs[node] = {}
        if node not in self.heuristics:
            self.heuristics[node] = 0

    def add_edge(self, from_node, to_node, cost):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append(to_node)
        self.costs[from_node][to_node] = cost

    # Add the straight-line distance (SLD) heuristic from each node to the goal node (E). 
    def add_heuristic(self, node, heuristic):
        self.heuristics[node] = heuristic


# Takes the graph, start, and goal as inputs
# Returns the shortest path between start and goal as well as the cost of that path.
def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.edges[current]:
            new_cost = cost_so_far[current] + graph.costs[current][next]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + graph.heuristics[next]
                frontier.put(next, priority)
                came_from[next] = current

    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()

    return path, cost_so_far[goal]

# Example usage (the graph has five nodes (A, B, C, D, and E) and seven edges with their costs
# 
#   [A]---(5)---[B]--_
#   |  \__       |   (3)_
#  (2)    (6)__ (4)     _[C]
#   |          \_|  _(8)
#   [B]---(7)---[D]/
#

graph = Graph()
graph.add_edge('A', 'B', 5)
graph.add_edge('A', 'E', 2)
graph.add_edge('A', 'D', 6)
graph.add_edge('B', 'C', 3)
graph.add_edge('B', 'D', 4)
graph.add_edge('C', 'D', 8)
graph.add_edge('D', 'E', 7)

graph.add_heuristic('A', 2)
graph.add_heuristic('B', 3)
graph.add_heuristic('C', 3)
graph.add_heuristic('D', 4)
graph.add_heuristic('E', 2)

start = 'A'
goal = 'D'
path, cost = a_star_search(graph, start, goal)

print("Shortest path from", start, "to", goal, ":", path)
print("Cost:", cost)