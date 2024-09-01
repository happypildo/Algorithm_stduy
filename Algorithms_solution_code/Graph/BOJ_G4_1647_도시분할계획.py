"""
# 문제 링크: https://www.acmicpc.net/problem/1647

# 문제 설명:
- 집들이 있고, 집을 잇는 길들이 있다.
- 집을 잇는 길들은 각각 관리 비용이 존재하는데, 이를 최소화하고자 한다.
- 최소화하면서, 집들을 두 마을로 구분하고자 하는데 두 마을이라 함은 각 마을의 집들이 서로 연결되지 않음을 의미한다.
- 집을을 두 마을로 구성하면서, 관리 비용을 최소화할 때 해당 관리 비용을 출력하시오.

# 접근 방법:
- 간선의 개수가 1,000,000까지이기 때문에 PRIM 알고리즘을 활용했습니다.
- 알고리즘 수행 시, 결국 모든 집들이 하나의 간선들로 연결이 되기 때문에
- 마을을 구성하는 것은 구성된 MST에서 최대 가중치를 빼는 방식으로 했습니다.
"""

import heapq

def prim(graph):
    # 노드들을 순회하면서 간선을 하나 씩 선택해 나가는 방식
    start_node = 1
    min_heap = []
    for e, w in graph[start_node]:
        heapq.heappush(min_heap, [w, e])
    is_visited = set()
    is_visited.add(start_node)

    answer = 0
    max_val = -1
    while min_heap:
        w, e = heapq.heappop(min_heap)
        if e not in is_visited:
            is_visited.add(e)
            answer += w
            if max_val < w:
                max_val = w
            for neighbor, weight in graph[e]:
                if neighbor in is_visited: continue
                heapq.heappush(min_heap, [weight, neighbor])
    
    return answer - max_val

N, M = list(map(int, input().split()))
graph = {x: [] for x in range(1, N+1)}
for _ in range(M):
    s, e, w = list(map(int, input().split()))
    graph[s].append((e, w))
    graph[e].append((s, w))

answer = prim(graph)
# answer = split_town(MST)
print(answer)