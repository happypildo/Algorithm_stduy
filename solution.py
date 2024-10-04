DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
PUT_LOCATIONS = set()
RESULT = 0


def update_impossible_loc(N, impossible_location_set, cur_point):
    temp_location_set = impossible_location_set | {cur_point}
    for dx, dy in DIRECTION:
        temp_x, temp_y = cur_point[0] + dx, cur_point[1] + dy

        while (-1 < temp_x < N) and (-1 < temp_y < N):
            temp_location_set.add((temp_x, temp_y))
            temp_x, temp_y = temp_x + dx, temp_y + dy

    return temp_location_set


SELECTED = set()
def DFS(N, all_location_set, impossible_location_set, put_location, depth, selected_set):
    global RESULT
    global PUT_LOCATIONS
    global SELECTED

    if depth == N:
        RESULT += 1
        SELECTED.add(tuple(selected_set))
        return
    if len(all_location_set - impossible_location_set) == 0:
        return

    temp_location_set = update_impossible_loc(N, impossible_location_set, put_location)
    for loc in all_location_set - temp_location_set:
        temp_selected_set = selected_set | {put_location}
        DFS(N, all_location_set, temp_location_set, loc, depth + 1, temp_selected_set)


chess_size = int(input())
all_loc = set([
    (i, j) for j in range(chess_size) for i in range(chess_size)
])

for i in range(chess_size // 2):
    for j in range(i + 1):
        print((i, j))
        DFS(chess_size, all_loc, set(), (i, j), 1, {(i, j)})
print(RESULT)
print(len(SELECTED))
