"""
서로소 집합은 두 집합의 교집합이 공집합일 경우를 의미한다.
그래프 이론에서, 두 집합이 서로소 집합 관계일 때 두 집합 내 어떤 원소를 연결하든 사이클이 생기지 않는다.
반대로, 서로소 집합이 아닌 관계에서 연결 시 사이클이 발생한다.

이를 활용하기 위해 disjoint set의 대표자를 선정한다.
-> 대표자는 셋을 대표하는 어떠한 원소이기 때문에 이 것만을 비교하면 서로 서로소 집합 관계 여부를 알 수 있다.
"""

class DisjointSet:
    def __init__(self, n):
        self.p = [0] * (n + 1)
        self.r = [0] * (n + 1)

    def make_set(self, x):
        self.p[x] = x

    def find_set(self, x):
        if self.p[x] != x:
            self.p[x] = self.find_set(self.p, self.p[x])
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
