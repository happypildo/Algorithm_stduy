"""
PRIM 알고리즘 또한 MST를 찾는 알고리즘이다. 다른 점은 "정점"을 찾는 알고리즘이라는 것이다.
- 따라서, 노드가 적고 간선이 많다면 PRIM을 / 그 반대라면 Kruskal이 효율적일 수 있다.
"""
import heapq

def mst_prim(vertices, edges):
    adj_list = {v: [] for v in vertices}
    for s, e, w in edges:
        adj_list[s].append((e, w))
        adj_list[e].append((s, w))

    mst = []
    visited = set()
    init_vertex = vertices[0]
    min_heap = [(w, init_vertex, e) for w, e in adj_list[init_vertex]]
    heapq.heapify(min_heap)
    visited.add(init_vertex)

    while min_heap:
        w, s, e = heapq.heappop(min_heap)
        if e in visited: continue

        visited.add(e)
        mst.append((s, e, w))

        for adj_v, adj_w in adj_list[e]:
            if adj_v not in visited:
                heapq.heappush(min_heap, [adj_w, e, adj_v])
    return mst

edges = [[1, 2, 1], [2, 3, 3], [1, 3, 2]]
vertices = [1, 2, 3]
print(mst_prim(vertices, edges))