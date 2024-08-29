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


def bellman_ford(N, E, graph, start_point):
    distances = [float('inf') for _ in range(N + 1)]
    distances[start_point] = 0

    for _ in range(N):
        is_updated = False
        for node in range(N + 1):
            for end_node, weight in graph[node]:
                incoming_cost = distances[node] + weight
                prev_cost = distances[end_node]
                if incoming_cost != float('inf') and incoming_cost < prev_cost:
                    distances[end_node] = incoming_cost
                    is_updated = True
            
        if not is_updated: break

    # 음수 사이클이 존재하는지 확인해보자.
    for node in range(N + 1):
        for end_node, weight in graph[node]:
            incoming_cost = distances[node] + weight
            prev_cost = distances[end_node]
            if incoming_cost != float('inf') and incoming_cost < prev_cost:
                return -1
    
    return distances

def floyd(N, E, graph, start_point):
    DP = [[float('inf') for _ in range(N + 1)] for _ in range(N + 1)]

    for s in graph.keys():
        DP[s][s] = 0
        for e, w in graph[s]:
            DP[s][e] = w
    
    for stopover in range(N + 1):
        for s in range(N + 1):
            for e in range(N + 1):
                if s == stopover or e == stopover: continue

                DP[s][e] = min(
                    DP[s][e],
                    DP[s][stopover] + DP[stopover][e]
                )
    
    return DP


T = int(input())

for t_iter in range(1, T+1):
    N, E = list(map(int, input().split()))

    graph = {x: [] for x in range(N + 1)}
    for e in range(E):
        s, e, w = list(map(int, input().split()))
        graph[s].append((e, w))
    
    # Dijkstra
    # distances = dijkstra(N, E, graph, 0)
    # print(f"#{t_iter} {distances[N]}")

    # Bellman-Ford
    # distances = bellman_ford(N, E, graph, 0)
    # answer = -1 if distances == -1 else distances[N]
    # print(f"#{t_iter} {answer}")

    # Floyd
    DP = floyd(N, E, graph, 0)
    answer = DP[0][N]
    print(f"#{t_iter} {answer}")

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