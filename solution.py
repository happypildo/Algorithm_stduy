path_dict = {}
rev_path_dict = {}
visited_set = set()
rev_visited_set = set()
def DFS(graph, node, target_node, is_visited, re=False, is_reverse=False):
    global visited_set
    global rev_visited_set
    global path_dict
    global rev_path_dict

    if node == target_node and not re:
        if is_reverse:
            for i in range(len(is_visited)):
                if rev_path_dict.get(is_visited[i], None) is None:
                    # i번째 노드로 가면 이렇게 갈 수 있어요!
                    rev_path_dict[is_visited[i]] = is_visited[i+1:]
                else:
                    rev_path_dict[is_visited[i]].append(is_visited[i+1:])
            rev_visited_set = rev_visited_set | set(is_visited)
            return True
        else:
            for i in range(len(is_visited)):
                if path_dict.get(is_visited[i], None) is None:
                    # i번째 노드로 가면 이렇게 갈 수 있어요!
                    path_dict[is_visited[i]] = is_visited[i+1:]
                else:
                    path_dict[is_visited[i]].append(is_visited[i+1:])
            visited_set = visited_set | set(is_visited)
            return True
    if path_dict.get(node, None) is not None and not is_reverse:
        visited_set = visited_set | set(is_visited)
        return True
    if rev_path_dict.get(node, None) is not None and is_reverse:
        rev_visited_set = rev_visited_set | set(is_visited)
        return True

    ret = False
    for neighbor in graph[node]:
        if neighbor not in is_visited:
            temp_is_visited = is_visited[:]
            temp_is_visited.append(neighbor)
            ret = ret | DFS(graph, neighbor, target_node, temp_is_visited, re, is_reverse)
    return ret

def reDFS(graph, target_node, dict_key, is_reverse):
    if is_reverse:
        for key in dict_key:
            if key == target_node: continue
            for neighbor in graph[key]:
                if neighbor in dict_key: continue
                else:
                    if DFS(graph, neighbor, target_node, [], True, is_reverse):
                        rev_visited_set.add(neighbor)
    else:
        for key in dict_key:
            if key == target_node: continue
            for neighbor in graph[key]:
                if neighbor in dict_key: continue
                else:
                    if DFS(graph, neighbor, target_node, [], True, is_reverse):
                        visited_set.add(neighbor)

N, M = list(map(int, input().split()))

graph = {}

for _ in range(M):
    s, e = list(map(int, input().split()))
    if graph.get(s, None) is None: graph[s] = [e]
    else: graph[s].append(e)

S, T = list(map(int, input().split()))

DFS(graph, S, T, [S], False, False)
reDFS(graph, T, set(path_dict.keys()), False)

DFS(graph, T, S, [T], False, True)
reDFS(graph, S, set(rev_path_dict.keys()), True)

print(len(visited_set & rev_visited_set) - 2)
