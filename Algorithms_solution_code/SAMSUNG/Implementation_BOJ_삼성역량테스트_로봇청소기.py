DIRECTION = [[0, -1, 0], [1, 0, 1], [2, 1, 0], [3, 0, -1]]


def dfs(room_map, point, is_visited, heading):
    x, y = point

    # 현재 칸 청소
    if room_map[x][y] == 0:
        room_map[x][y] = 2

    jud = False
    for _, dx, dy in DIRECTION:
        temp_x, temp_y = x + dx, y + dy
        if (-1 < temp_x < len(room_map)) and (-1 < temp_y < len(room_map[0])):
            if room_map[temp_x][temp_y] == 0:
                jud = True

    if jud:
        # 청소할 곳이 있다면? -> 반시계 방향으로 회전하면서
        dynamic_direction = DIRECTION[heading:] + DIRECTION[:heading]
        dynamic_direction = dynamic_direction[::-1]
        for idx, dx, dy in dynamic_direction:
            temp_x, temp_y = x + dx, y + dy

            if (-1 < temp_x < len(room_map)) and (-1 < temp_y < len(room_map[0])):
                if room_map[temp_x][temp_y] == 0:
                    dfs(room_map, (temp_x, temp_y), is_visited, idx)
                    break
    else:
        x, y = x - DIRECTION[heading][1], y - DIRECTION[heading][2]
        if (-1 < x < len(room_map)) and (-1 < y < len(room_map[0])):
            if room_map[x][y] != 1:
                dfs(room_map, (x, y), is_visited, heading)


N, M = list(map(int, input().split()))

r, c, d = list(map(int, input().split()))

room = [list(map(int, input().split())) for _ in range(N)]

room[r][c] = 2
dfs(room, (r, c), set(), d)

answer = 0
for i in range(N):
    for j in range(M):
        if room[i][j] == 2:
            answer += 1
print(answer)