"""
# 문제 링크: https://www.acmicpc.net/problem/11403
# 문제 설명:
- 무방향 그래프가 주어졌을 때, i->j로 가는 길이가 양수인 경로가 있는지 없는지 구하시오.
# 접근법:
- 모든 정점 쌍에 대한 거리를 구해야 하기 때문에 Floyd 알고리즘을 사용함
"""

N = int(input())
graph = [list(map(int, input().split())) for _ in range(N)]

for i in range(N):
    for j in range(N):
        if graph[i][j] == 0: graph[i][j] = float('inf')

for stopover in range(N):
    for i in range(N):
        for j in range(N):
            if i == stopover or j == stopover: continue
            graph[i][j] = min(
                graph[i][j],
                graph[i][stopover] + graph[stopover][j]
            )


for i in range(N):
    for j in range(N):
        answer = 1 if graph[i][j] != float('inf') else 0
        print(answer, end=" ")
    print()