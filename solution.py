highest_delay = -1
MEMOIZATION = {}
def DFS(delay_list, graph, start_point):
    global highest_delay
    global MEMOIZATION

    if MEMOIZATION.get(start_point, None) is not None:
        return MEMOIZATION[start_point]
    
    delay = delay_list[start_point - 1]
    ret = []
    for neighbor in graph[start_point]:
        ret.append(DFS(delay_list, graph, neighbor))
    
    if len(ret) == 0:
        MEMOIZATION[start_point] = delay
    else:
        ret = [item + delay for item in ret]
        delay = max(ret)
        MEMOIZATION[start_point] = delay
    return MEMOIZATION[start_point]

T = int(input())

for t_iter in range(1, T+1):
    highest_delay = -1
    MEMOIZATION = {}
    N, K = list(map(int, input().strip().split()))

    build_delay = list(map(int, input().strip().split()))

    dependency_graph = {x+1: set() for x in range(N)}
    for k_iter in range(K):
        from_building, to_building = list(map(int, input().split()))
        dependency_graph[to_building].add(from_building)
    target_building = int(input())

    DFS(build_delay, dependency_graph, target_building)
    print(MEMOIZATION[target_building])