# https://www.acmicpc.net/problem/1753

import heapq
def dijkstra(graph, start_node):
    distances = [float('inf') for _ in range(len(graph) + 1)]
    distances[0] = 0
    distances[start_node] = 0

    min_heap = []
    heapq.heappush(min_heap, [0, start_node])

    while min_heap:
        curr_dist, node = heapq.heappop(min_heap)

        for neighbor, weight in graph[node]:
            incoming_distance = curr_dist + weight
            original_distance = distances[neighbor]
            if incoming_distance < original_distance:
                distances[neighbor] = incoming_distance
                heapq.heappush(min_heap, [incoming_distance, neighbor])

    return distances


def bellman_ford(graph, start_node):
    distances = [float('inf') for _ in range(len(graph) + 1)]
    distances[0] = 0
    distances[start_node] = 0

    for i in range(len(graph) - 1):         # 우선  V-1번 순회한다.
        is_changed = False
        for v in graph.keys():
            for e, w in graph[v]:
                incoming_distance = distances[v] + w
                original_distance = distances[e]
                if incoming_distance < original_distance:
                    distances[e] = incoming_distance
                    is_changed = True
        if not is_changed: break

    # 음수 사이클이 존재할 수 있으니, 한 번 더 순회해본다.
    for v in graph.keys():
        for e, w in graph[v]:
            incoming_distance = distances[v] + w
            original_distance = distances[e]
            if incoming_distance < original_distance:
                # 음수 사이클이 존재함을 의미한다.
                return -1

    return distances


V, E = list(map(int, input().split()))

start_node = int(input())

graph = {x + 1: [] for x in range(V)}
for _ in range(E):
    s, e, w = list(map(int, input().split()))
    graph[s].append((e, w))

# distances = dijkstra(graph, start_node)
distances = bellman_ford(graph, start_node)
answer = []
for val in distances[1:]:
    answer.append(str(val) if val != float('inf') else "INF")
print("\n".join(answer))
