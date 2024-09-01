"""
# 문제 링크: https://www.acmicpc.net/problem/11403
# 문제 설명:
- 무방향 그래프가 주어졌을 때, i->j로 가는 최소 길이를 모두 구하시오.
# 접근법:
- 모든 정점 쌍에 대한 거리를 구해야 하기 때문에 Floyd 알고리즘을 사용함
"""

def floyd():
    pass

N = int(input())
M = int(input())

graph = [[float('inf') for _ in range(N + 1)] for _ in range(N + 1)]
for m_iter in range(M):
    s, e, w = list(map(int, input().split()))
    graph[s][e] = graph[s][e] if graph[s][e] < w else w

for stopover in range(1, N + 1):
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if i == stopover or j == stopover or i == j: continue
            graph[i][j] = min(
                graph[i][j],
                graph[i][stopover] + graph[stopover][j]
            )            


for i in range(1, N + 1):
    for j in range(1, N + 1):
        answer = graph[i][j] if graph[i][j] != float('inf') else 0
        print(answer, end=" ")
    print()