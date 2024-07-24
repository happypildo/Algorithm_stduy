N = 7

graph = {
    0: [1, 2, 3],
    1: [0, 4],
    2: [0, 5],
    3: [0, 6],
    4: [1],
    5: [2],
    6: [3]
}

is_visited = [0 for _ in range(N)]

def DFS(node):
    global graph
    global is_visited

    print(f"{node} - ", end="")

    for to_go in graph[node]:
        if is_visited[to_go] == 0:
            is_visited[to_go] = 1
            DFS(to_go)

is_visited[0] = 1
DFS(0)
print("END")