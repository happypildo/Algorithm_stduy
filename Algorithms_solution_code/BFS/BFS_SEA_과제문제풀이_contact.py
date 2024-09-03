from collections import deque

def BFS(graph, start_node):
    depth_dict = {0: [start_node]}
    max_depth = 0
    
    queue = deque()
    queue.append((start_node, 0))
    
    is_visited = set()
    is_visited.add(start_node)
    
    while queue:
        item, depth = queue.popleft()
        
        if graph.get(item, None) is None: continue
        for neighbor in graph[item]:
            if neighbor in is_visited: continue
            is_visited.add(neighbor)
            queue.append((neighbor, depth+1))
            max_depth = depth + 1 if max_depth < depth + 1 else max_depth
            if depth_dict.get(depth+1, None) is None:
                depth_dict[depth+1] = [neighbor]
            else:
                depth_dict[depth+1].append(neighbor)
    
    return max(depth_dict[max_depth])


T = 10

for t_iter in range(1, T+1):
    N, start = list(map(int, input().split()))
    
    graph = {}
    data = list(map(int, input().split()))
    for idx in range(N // 2):
        from_node = data[idx * 2]
        to_node = data[idx * 2 + 1]
        
        if graph.get(from_node, None) is None:
            graph[from_node] = set([to_node])
        else:
            graph[from_node].add(to_node)
    
    answer = BFS(graph, start)
    print(f"#{t_iter} {answer}")
