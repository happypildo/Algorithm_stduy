import heapq

def dijkstra(N, E, graph, start_point):
    distances = [float('inf') for _ in range(N + 1)]
    distances[start_point] = 0
    
    min_heap = []
    heapq.heappush(min_heap, [0, start_point])

    while min_heap:
        curr_dist, node = heapq.heappop(min_heap)

        for neighbor in graph[node]:
            e, w = neighbor
            if curr_dist + w < distances[e]:
                distances[e] = curr_dist + w
                heapq.heappush(min_heap, [distances[e], e])

    return distances

T = int(input())

for t_iter in range(1, T+1):
    N, E = list(map(int, input().split()))

    graph = {x: [] for x in range(N + 1)}
    for e in range(E):
        s, e, w = list(map(int, input().split()))
        graph[s].append((e, w))
    
    # Dijkstra
    distances = dijkstra(N, E, graph, 0)
    print(f"#{t_iter} {distances[N]}")

"""
3
2 3
0 1 1
0 2 6
1 2 1
4 7
0 1 9
0 2 3
0 3 7
1 4 2
2 3 8
2 4 1
3 4 8
4 6
0 1 10
0 2 7
1 4 2
2 3 10
2 4 3
3 4 10
"""