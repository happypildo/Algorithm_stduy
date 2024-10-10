from itertools import product

CAMERA_AREA = {
    1: [
        [[0, 1]], [[1, 0]], [[0, -1]], [[-1, 0]]
    ],
    2: [
        [[0, 1], [0, -1]], [[1, 0], [-1, 0]]
    ],
    3: [
        [[-1, 0], [0, 1]], [[0, 1], [1, 0]], [[1, 0], [0, -1]], [[0, -1], [-1, 0]]
    ],
    4: [
        [[0, -1], [-1, 0], [0, 1]], [[-1, 0], [0, 1], [1, 0]], [[0, 1], [1, 0], [0, -1]], [[1, 0], [0, -1], [-1, 0]]
    ],
    5: [
        [[0, 1], [1, 0], [0, -1], [-1, 0]]
    ]
}

N, M = list(map(int, input().split()))

office = [list(map(int, input().split())) for _ in range(N)]

loc_of_walls = set()
loc_of_cctvs = []

answer = float('inf')
for i in range(N):
    for j in range(M):
        if office[i][j] == 6:
            loc_of_walls.add((i, j))
        elif office[i][j] > 0:
            loc_of_cctvs.append((len(loc_of_cctvs), i, j, office[i][j]))

possible_rotation = [[0, 1, 2, 3] for _ in range(len(loc_of_cctvs))]

for prod in product(*possible_rotation):
    temp_map = [office[i][:] for i in range(N)]
    areas = []
    cannot = False
    for camera_idx, rotation_cnt in enumerate(prod):
        camera_type = loc_of_cctvs[camera_idx][3]
        rotation_types = CAMERA_AREA[camera_type]

        if rotation_cnt > len(rotation_types) - 1:
            cannot = True
            break

        areas.append(rotation_types[rotation_cnt])

    if cannot:
        continue

    for camera_idx, area in enumerate(areas):
        for dx, dy in area:
            temp_x, temp_y = loc_of_cctvs[camera_idx][1:3]
            temp_x, temp_y = temp_x + dx, temp_y + dy

            while (-1 < temp_x < N) and (-1 < temp_y < M):
                if office[temp_x][temp_y] == 6:
                    break

                temp_map[temp_x][temp_y] = '#'

                temp_x, temp_y = temp_x + dx, temp_y + dy

    cnt = 0
    for i in range(N):
        for j in range(M):
            if temp_map[i][j] == 0:
                cnt += 1
    if answer > cnt:
        answer = cnt

print(answer)