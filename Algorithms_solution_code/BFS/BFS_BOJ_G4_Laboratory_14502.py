from itertools import combinations
from collections import deque

DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]


def BFS(N, M, lab, start_point):
    is_visited = {start_point, }
    queue = deque([start_point])

    while queue:
        x, y = queue.popleft()

        for dx, dy in DIRECTION:
            temp_x, temp_y = x + dx, y + dy
            if (-1 < temp_x < N) and (-1 < temp_y < M):
                if lab[temp_x][temp_y] != 0:
                    continue
                if (temp_x, temp_y) in is_visited:
                    continue

                lab[temp_x][temp_y] = 2
                queue.append((temp_x, temp_y))
                is_visited.add((temp_x, temp_y))

    return lab


N, M = list(map(int, input().split()))
lab = [list(map(int, input().split())) for _ in range(N)]
loc_of_virus = []
hall = []
for n in range(N):
    for m in range(M):
        if lab[n][m] == 0:
            hall.append((n, m))
        elif lab[n][m] == 2:
            loc_of_virus.append((n, m))

ret = 0
for comb in combinations(hall, 3):
    temp_lab = [lab[i][:] for i in range(N)]
    for w in comb:
        temp_lab[w[0]][w[1]] = 1
    for v in loc_of_virus:
        temp_lab = BFS(N, M, temp_lab, v)

    cnt = 0
    for i in range(N):
        for j in range(M):
            if temp_lab[i][j] == 0:
                cnt += 1
    ret = max(ret, cnt)

print(ret)