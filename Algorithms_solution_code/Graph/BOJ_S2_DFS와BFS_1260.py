def DFS(graph, start_node, is_visited):
    ret = []

    for neighbor in graph[start_node]:
        if neighbor in is_visited: continue
        is_visited.append(neighbor)
        ret = ret + [neighbor] + DFS(graph, neighbor, is_visited)

    return ret


from collections import deque
def BFS(graph, start_node):
    queue = deque()
    queue.append(start_node)

    is_visited = [start_node]

    while queue:
        item = queue.popleft()

        for neighbor in graph[item]:
            if neighbor in is_visited: continue
            queue.append(neighbor)
            is_visited.append(neighbor)

    return is_visited


def solve():
    N, M, V = list(map(int, input().split()))
    graph = {x: [] for x in range(1, N + 1)}
    for _ in range(M):
        s, e = list(map(int, input().split()))
        graph[s].append(e)
        graph[e].append(s)
    
    for key in graph.keys():
        graph[key] = sorted(graph[key])

    result_DFS = [V] + DFS(graph, V, [V])
    result_BFS = BFS(graph, V)

    ret = ""
    for x in result_DFS:
        ret += str(x) + " "
    ret = ret + "\n"
    for x in result_BFS:
        ret += str(x) + " "
    ret = ret + "\n"
    print(ret)


solve()