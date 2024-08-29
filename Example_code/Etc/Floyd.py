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

    # Floyd
    DP = floyd(N, E, graph, 0)
    answer = DP[0][N]
    print(f"#{t_iter} {answer}")