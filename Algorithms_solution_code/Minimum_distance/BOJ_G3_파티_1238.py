"""
# 문제 링크: https://www.acmicpc.net/problem/11403
# 문제 설명:
- 방향 그래프가 주어질 때, X 노드를 기준으로 왔다 갔다 거리가 가장 긴 거리를 계산하시오.
# 접근 방법:
- 처음에는 Floyd를 사용했는데 시간 초과가 났습니다. (다익스트라랑 똑같은데 왜지티비;)
- 그래서, 기존 그래프로 X부터 시작해 최단 거리를 구하는 다익스트라, 그래프를 역전시켜서 X로 가게되는 최단 거리를 구하는 다익스트라를 돌려 구했습니다.
"""
import heapq

def dijkstra(graph, X):
    distances = [float('inf') for _ in range(N + 1)]
    distances[X] = 0

    min_heap = []
    heapq.heappush(min_heap, [0, X])

    while min_heap:
        cur_dist, cur_node = heapq.heappop(min_heap)

        for neighbor, weight in graph[cur_node]:
            incoming = cur_dist + weight
            original = distances[neighbor]
            if incoming < original:
                distances[neighbor] = incoming
                heapq.heappush(min_heap, [distances[neighbor], neighbor])

    return distances

N, M, X = list(map(int, input().split()))
graph = {x: [] for x in range(1, N+1)}
rev_graph = {x: [] for x in range(1, N+1)}
for _ in range(M):
    s, e, w = list(map(int, input().split()))
    graph[s].append((e, w))
    rev_graph[e].append((s, w))

distances = dijkstra(graph, X)
rev_distances = dijkstra(rev_graph, X)

answer = -1
for a, b in zip(distances, rev_distances):
    if a == float('inf') or b == float('inf'): continue
    answer = a + b if answer < a + b else answer
print(answer)