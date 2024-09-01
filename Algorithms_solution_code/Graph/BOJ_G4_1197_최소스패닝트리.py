class DisjointSet:
    def __init__(self, V):
        self.represents = [x for x in range(V + 1)]
        self.rank = [0] * (V + 1)
    
    def find_set(self, x):
        if x != self.represents[x]:
            self.represents[x] = self.find_set(self.represents[x])
        return self.represents[x]

    def union(self, x, y):
        rep_x, rep_y = self.represents[x], self.represents[y]
        if self.rank[rep_x] > self.rank[rep_y]:
            self.represents[rep_y] = rep_x
        elif self.rank[rep_x] < self.rank[rep_y]:
            self.represents[rep_x] = rep_y
        else:
            self.represents[rep_x] = rep_y
            self.rank[rep_y] += 1            


V, E = list(map(int, input().split()))
graph = sorted([list(map(int, input().split())) for _ in range(E)], key=lambda x: x[2])

ds = DisjointSet(V)

answer = 0
for s, e, w in graph:
    if ds.find_set(s) != ds.find_set(e):
        ds.union(s, e)
        answer += w

print(answer)