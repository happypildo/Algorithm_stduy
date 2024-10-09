from itertools import combinations

DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]
POSSIBLE_SHAPES = set()


def dfs(point, is_visited, depth):
    if depth == 3:
        POSSIBLE_SHAPES.add(tuple(is_visited))
        return

    x, y = point
    for dx, dy in DIRECTION:
        temp_x, temp_y = x + dx, y + dy

        if (temp_x, temp_y) in is_visited:
            continue

        temp_is_visited = is_visited | {(temp_x, temp_y)}
        dfs((temp_x, temp_y), temp_is_visited, depth+1)


def search_specific(N, M, point, number_map):
    m_value = -1
    i, j = point
    for shape in combinations(DIRECTION, 3):
        shape = list(shape) + [[0, 0]]

        value = 0
        for dx, dy in shape:
            temp_x, temp_y = i + dx, j + dy

            if (-1 < temp_x < N) and (-1 < temp_y < M):
                value += number_map[temp_x][temp_y]
            else:
                break

        if m_value < value:
            m_value = value

    return m_value


dfs((0, 0), {(0, 0)}, 0)

N, M = list(map(int, input().split()))
input_map = [list(map(int, input().split())) for _ in range(N)]

m_value = -1
for i in range(N):
    for j in range(M):
        for shape in POSSIBLE_SHAPES:
            value = 0
            cnt = 0
            for dx, dy in shape:
                temp_x, temp_y = i + dx, j + dy

                if (-1 < temp_x < N) and (-1 < temp_y < M):
                    value += input_map[temp_x][temp_y]
                    cnt += 1
                else:
                    break

            if m_value < value and cnt == 4:
                m_value = value

        value = search_specific(N, M, (i, j), input_map)
        if m_value < value:
            m_value = value

print(m_value)


