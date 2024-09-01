"""
# 문제 링크: https://www.acmicpc.net/problem/16398
# 문제 설명: 
- N개의 행성이 있고, 이 행성을 잇고자 한다. 그러나 행성을 잇고 나면 유지 비용을 내야한다.
- 모든 행성을 잇고 싶은데, 유지 비용을 최소화하고 싶다.
- 이 때의 유지 비용을 출력하시오.

# 접근 방법:
- 먼저, 간선의 개수가 매우 많기 떄문에 PRIM 알고리즘을 썻었습니다. (간선 수: N * (N - 1) / 2)
- 공부 삼아, Kruskal로도 작성을 해 보았는데, 
    - PRIM: 2524 ms
    - Kruskal: 2168 ms
    가 나왔습니다.
- 아마 이는 Kruskal 시 진행하는 정렬 알고리즘의 힘이 쎈 것 같습니다.
"""

class DisjointSet:
    def __init__(self, N):
        self.represents = [x for x in range(N)]
        self.rank = [0] * (N)

    def find_set(self, x):
        if self.represents[x] != x:
            self.represents[x] = self.find_set(self.represents[x])
        return self.represents[x]

    def union(self, x, y):
        rep_x, rep_y = self.represents[x], self.represents[y]
        if rep_x != rep_y:
            if self.rank[rep_x] > self.rank[rep_y]:
                self.represents[rep_y] = rep_x
            elif self.rank[rep_x] < self.rank[rep_y]:
                self.represents[rep_x] = rep_y
            else:
                self.represents[rep_x] = rep_y
                self.rank[rep_y] += 1


N = int(input())
distances = []
for i in range(N):
    for j, val in enumerate(list(map(int, input().strip().split()))):
        distances.append([val, i, j])
distances = sorted(distances, key=lambda x: x[0])

answer = 0
ds = DisjointSet(N)
for w, s, e in distances:
    if ds.find_set(s) != ds.find_set(e):
        ds.union(s, e)
        answer += w

print(answer)