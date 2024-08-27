"""
크루스칼 알고리즘은 MST를 만드는 알고리즘 중 하나이다.
연결되어 있는 많은 간선 중 "가장 작은 가중치"를 갖는 간선을 탐욕적으로 선택한다.
이 때, 사이클이 생성되지 않도록 서로소 집합 개념을 사용한다.
"""
class DisjointSet:
    def __init__(self, n):
        self.p = [0] * (n + 1)
        self.r = [0] * (n + 1)

    def make_set(self, x):
        self.p[x] = x

    def find_set(self, x):
        if self.p[x] != x:
            self.p[x] = self.find_set(self.p[x])
        return self.p[x]

    def union(self, x, y):
        px = self.p[x]
        py = self.p[y]

        if px == py:
            # 이 둘은 같은 집합에 이미 속해 있다.
            pass
        else:
            if self.r[px] > self.r[py]:
                # 트리가 깊어지는 것을 방지하기 위해서, 낮은 랭크를 갖는 것을 붙인다.
                self.p[py] = px
            elif self.r[x] < self.r[py]:
                self.p[px] = py
            else:
                self.p[py] = px
                self.r[px] += 1


def mst_kruskal(vertices, edges):
    # 정점들을 서로소 집합에 넣는다.
    mst = []
    disjoint_set = DisjointSet(len(vertices))
    for v in vertices:
        disjoint_set.make_set(v)
    sorted_edges = sorted(edges, key=lambda x:x[2])     # 간선의 가중치를 기반으로 정렬을 진행한다.

    cnt = 0
    while len(mst) < len(vertices) - 1:
        s, e, w = sorted_edges[cnt]
        # 시작 정점과 끝 정점이 서로소 집합 관계여야 한다.
        if disjoint_set.find_set(s) != disjoint_set.find_set(e):
            # 이를 채택했으니, 하나의 집합으로 만든다.
            disjoint_set.union(s, e)
            mst.append(sorted_edges[cnt])

        cnt += 1

    return mst

edges = [[1, 2, 1], [2, 3, 3], [1, 3, 2]]
vertices = [1, 2, 3]
print(mst_kruskal(vertices, edges))