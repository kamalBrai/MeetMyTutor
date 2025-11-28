import heapq

def dijkstra(graph, start):
    """
    Compute shortest distances from start node to all other nodes in the graph.

    Parameters:
    - graph: dict of adjacency list { node: [(neighbor, weight), ...], ... }
    - start: start node (e.g., 'student')

    Returns:
    - distances: dict { node: shortest distance from start }
    - previous: dict { node: previous node on shortest path }
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}

    heap = [(0, start)]  # priority queue of (distance, node)

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(heap, (distance, neighbor))

    return distances, previous
