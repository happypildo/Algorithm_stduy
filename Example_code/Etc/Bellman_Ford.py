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


T = int(input())

for t_iter in range(1, T+1):
    N, E = list(map(int, input().split()))

    graph = {x: [] for x in range(N + 1)}
    for e in range(E):
        s, e, w = list(map(int, input().split()))
        graph[s].append((e, w))
    
    # Bellman-Ford
    distances = bellman_ford(N, E, graph, 0)
    answer = -1 if distances == -1 else distances[N]
    print(f"#{t_iter} {answer}")