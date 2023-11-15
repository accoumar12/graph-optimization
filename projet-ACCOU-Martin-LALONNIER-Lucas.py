import heapq
import time

import matplotlib.pyplot as plt
import networkx as nx

# %% [markdown]
# ## Q1: We will use the networkx library, and we will first recreate the graph from the lecture slides.

# %%
g = nx.Graph(
    [
        ("1", "2", {"weight": 5}),
        ("2", "4", {"weight": 4}),
        ("4", "3", {"weight": 2}),
        ("3", "1", {"weight": 2}),
        ("W", "1", {"weight": 1}),
        ("W", "2", {"weight": 5}),
        ("W", "4", {"weight": 4}),
        ("W", "3", {"weight": 3}),
        ("1", "4", {"weight": 5}),
        ("3", "2", {"weight": 3}),
    ]
)
nx.draw_networkx(g, pos=nx.shell_layout(g))
nx.draw_networkx_edge_labels(
    g,
    pos=nx.shell_layout(g),
    edge_labels=dict(((u, v), g[u][v]["weight"]) for u, v in g.edges),
)

# %%
g["1"].items()

# %% [markdown]
# ## Q2: We implement Prim's algorithm.


# %%
def prim(graph):
    mst = nx.Graph()  # Initialize an empty graph for the Minimum Spanning Tree
    start_node = list(graph.nodes())[0]  # Start from the first node

    # Create a set to keep track of visited nodes
    visited = set([start_node])

    while len(visited) < len(graph.nodes()):
        min_edge = None
        min_cost = float("inf")

        for u in visited:
            for v, edge_data in graph[u].items():
                # print(u, v, edge_data['weight'])
                if v not in visited and edge_data["weight"] < min_cost:
                    min_edge = (u, v)
                    min_cost = edge_data["weight"]

        if min_edge:
            u, v = min_edge
            mst.add_edge(u, v, weight=min_cost)
            visited.add(v)

    return mst


# %%

mst = prim(g)
pos = nx.shell_layout(g)
nx.draw_networkx(g, pos=pos)
nx.draw_networkx_edge_labels(
    g, pos=pos, edge_labels={(u, v): d["weight"] for u, v, d in g.edges(data=True)}
)
nx.draw_networkx(mst, pos=pos, edge_color="r", width=2)
plt.show()

# %% [markdown]
# ## Q3: We can test on the edge.txt file.

# %%
with open("edges.txt", "r") as file:
    lines = file.readlines()
    num_vertices, num_edges = map(int, lines[0].split())

    # Create a new NetworkX graph
    g = nx.Graph()

    # Add edges to the graph from the file
    for line in lines[1:]:
        source, destination, cost = map(int, line.split())
        g.add_edge(source, destination, weight=cost)

# Apply Prim's algorithm to find the Minimum Spanning Tree
mst = prim(g)

# Calculate the sum of edge costs in the MST
total_cost = sum(data["weight"] for _, _, data in mst.edges(data=True))


# %% [markdown]
# ## Q4: We can implement a more advanced version using binary heaps.

# %%


def prim_binary_heap(graph):
    # Initialize
    mst = nx.Graph()
    nodes = list(graph.nodes())

    # Start from the first node: W
    start_node = nodes[0]
    size = len(graph.nodes())

    # Create a set to keep track of visited nodes
    visited = set([start_node])

    # Initialize the priority queue (binary heap)
    priority_queue = []

    # Helper function to add edges to the priority queue
    def add_edges_to_queue(node):
        for v, edge_data in graph[node].items():
            if v not in visited:
                heapq.heappush(priority_queue, (edge_data["weight"], node, v))

    add_edges_to_queue(start_node)

    while len(visited) < size:
        min_cost, u, v = heapq.heappop(priority_queue)
        if v not in visited:
            mst.add_edge(u, v, weight=min_cost)
            visited.add(v)
            add_edges_to_queue(v)

    return mst


# %%
mst_binary_heap = prim_binary_heap(g)

total_cost_binary_heap = sum(
    data["weight"] for _, _, data in mst_binary_heap.edges(data=True)
)


# %%

# Measure execution time for the optimized version (binary heap)
start_time = time.time()
mst = prim_binary_heap(g)
end_time = time.time()

print("Execution time (binary heap):", end_time - start_time, "seconds")
print("Sum of edge costs in MST (binary heap):", total_cost_binary_heap)

# Measure execution time for the naive version
start_time = time.time()
mst = prim(g)  # Run the naive version
end_time = time.time()

print("Execution time (naive):", end_time - start_time, "seconds")
print("Sum of edge costs in MST (naive)", total_cost)
