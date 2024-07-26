from collections import deque

# graph = {
#     0: [1, 2, 3],
#     1: [0, 4],
#     2: [0, 5],
#     3: [0, 6],
#     4: [1],
#     5: [2],
#     6: [3]
# }
graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4],
    3: [1, 5],
    4: [1, 2, 5],
    5: [3, 4, 6],
    6: [5]
}

def BFS(graph, start_node):
    result = [start_node]

    is_visited = set()
    is_visited.add(start_node)
    
    queue = deque([start_node])

    while queue:
        current_node = queue.popleft()

        for next_node in graph[current_node]:
            if next_node not in is_visited:
                queue.append(next_node)
                is_visited.add(next_node)
                result.append(next_node)

    return result

print(BFS(graph, 0))