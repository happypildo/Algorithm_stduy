import sys
sys.setrecursionlimit(10 ** 6)

original_path = [set(), set()]


def DFS(graph, graph_keys, node, start_node, target_node, is_visited, is_work):
    global original_path
    
    if target_node in original_path[is_work]:
        # 길은 하나 만 알고 있어도 된다.
        return
    
    if node not in graph_keys: return
    if node in original_path[is_work]: return
    if node == target_node:
        original_path[is_work].update(is_visited)
        original_path[is_work].add(node)
        return
        
    for neighbor in graph[node]:
        if neighbor not in is_visited:
            DFS(graph, graph_keys, neighbor, start_node, target_node, is_visited | set([neighbor]), is_work)

    return 

def reDFS(graph, graph_keys, cur_node, start_node, end_node, is_visited, is_work):
    global original_path
    
    # DFS를 돌면서 다시 original path로 회귀할 수 있는지 체크
    if cur_node in original_path[is_work]:
        return True
    
    ret = False
    if cur_node not in graph_keys: return False
    for neighbor in graph[cur_node]:
        if neighbor in is_visited: continue
        result = reDFS(graph, graph_keys, neighbor, start_node, end_node, is_visited | set([neighbor]), is_work)
        if result:
            original_path[is_work].add(neighbor)
        ret |= result
    if ret:
        original_path[is_work].add(cur_node)
    return ret
                
        

from collections import deque
def reBFS(graph, graph_keys, start_node, end_node):
    ret = []
    for i in [0, 1]:
        s = start_node if i == 0 else end_node
        e = end_node if i == 0 else start_node
        
        temp_original_path = original_path[i].copy()
        for path in temp_original_path:
            if path == e: continue
            for neighbor in graph[path]:
                if neighbor not in original_path:
                    reDFS(graph, graph_keys, neighbor, s, e, set(), i)

    return original_path
    

N, M = map(int,sys.stdin.readline().split())

graph = {}
graph_keys = set()
for _ in range(M):
    s, e = map(int,sys.stdin.readline().split())
    if graph.get(s, None) is None:
        graph[s] = set([e])
        graph_keys.add(s)
    else: 
        graph[s].add(e)

S, T = map(int,sys.stdin.readline().split())

DFS(graph, graph_keys, S, T, T, set([S]), 0)
DFS(graph, graph_keys, T, S, S, set([T]), 1)

ret = reBFS(graph, graph_keys, S, T)
print(len(ret[0] & ret[1]) - 2)