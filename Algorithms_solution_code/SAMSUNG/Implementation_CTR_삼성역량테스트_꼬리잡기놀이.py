from collections import deque

DIRECTION = [
    [-1, 0], [1, 0], [0, -1], [0, 1]
]


class Cluster:
    def __init__(self, game_map, idx, path):
        self.idx = idx
        self.path = path
        self.path_set = set(path)

        self.path_value = [game_map[x][y] for x, y in path]

        # 방향성 부여
        idx_of_head = self.path_value.index(1)
        idx_of_tail = self.path_value.index(3)

        self.direction = 1
        moving_idx = idx_of_tail + 1
        if moving_idx == len(path):
            moving_idx = 0
        if self.path_value[moving_idx] == 4 or self.path_value[moving_idx] == 1:
            # 거꾸로 가야한다.
            self.direction = -1

        self.numbering = [0 for _ in range(len(self.path))]
        if self.direction == -1:

            moving_idx = idx_of_head + 1
            self.numbering[idx_of_head] = 1
            numbering_idx = 2

            while True:
                if moving_idx == len(self.numbering):
                    moving_idx = 0

                if self.path_value[moving_idx] == 4 or self.path_value[moving_idx] == 1:
                    break

                self.numbering[moving_idx] = numbering_idx
                numbering_idx += 1
                moving_idx += 1
        elif self.direction == 1:

            moving_idx = idx_of_head - 1
            self.numbering[idx_of_head] = 1
            numbering_idx = 2

            while True:
                if moving_idx == -1:
                    moving_idx = len(self.numbering) - 1

                if self.path_value[moving_idx] == 4 or self.path_value[moving_idx] == 1:
                    break

                self.numbering[moving_idx] = numbering_idx
                numbering_idx += 1
                moving_idx -= 1

    def move(self):
        if self.direction == 1:
            self.path_value = [self.path_value[-1]] + self.path_value[:-1]
            self.numbering = [self.numbering[-1]] + self.numbering[:-1]
        else:
            self.path_value = self.path_value[1:] + [self.path_value[0]]
            self.numbering = self.numbering[1:] + [self.numbering[0]]

    def is_there(self, loc):
        if loc not in self.path_set:
            return -1

        line_idx = self.path.index(loc)
        if self.path_value[line_idx] == 4:
            return -1

        number = self.numbering[line_idx]

        # 방향 바꾸기
        self.direction *= -1
        # 머리 바꾸기
        idx_of_head = self.path_value.index(1)
        idx_of_tail = self.path_value.index(3)
        self.path_value[idx_of_head], self.path_value[idx_of_tail] = self.path_value[idx_of_tail], self.path_value[idx_of_head]

        self.numbering = [0 for _ in range(len(self.path))]

        if self.direction == -1:
            moving_idx = idx_of_tail + 1
            self.numbering[idx_of_tail] = 1
            numbering_idx = 2

            while True:
                if moving_idx == len(self.numbering):
                    moving_idx = 0

                if self.path_value[moving_idx] == 4 or self.path_value[moving_idx] == 1:
                    break

                self.numbering[moving_idx] = numbering_idx
                numbering_idx += 1
                moving_idx += 1
        elif self.direction == 1:
            moving_idx = idx_of_tail - 1
            self.numbering[idx_of_tail] = 1
            numbering_idx = 2

            while True:
                if moving_idx == -1:
                    moving_idx = len(self.numbering) - 1

                if self.path_value[moving_idx] == 4 or self.path_value[moving_idx] == 1:
                    break

                self.numbering[moving_idx] = numbering_idx
                numbering_idx += 1
                moving_idx -= 1

        return number ** 2


def bfs_to_find_path(map_size, start_point, paths, is_visited):
    queue = deque([start_point])
    prev_nodes = {start_point: None}

    while queue:
        x, y = queue.popleft()

        for dx, dy in DIRECTION:
            temp_x, temp_y = x + dx, y + dy

            if (temp_x, temp_y) not in paths:
                continue
            if (temp_x, temp_y) in is_visited:
                continue
            if (temp_x, temp_y) in prev_nodes:
                continue

            queue.append((temp_x, temp_y))
            prev_nodes[(temp_x, temp_y)] = (x, y)

    x, y = start_point
    target_point = -1
    for dx, dy in DIRECTION:
        temp_x, temp_y = x + dx, y + dy

        if (temp_x, temp_y) in prev_nodes[::-1]:
            target_point = (temp_x, temp_y)
            break

    path = [target_point]
    curr_node = prev_nodes[target_point]
    while curr_node is not None:
        path.append(curr_node)
        curr_node = prev_nodes[curr_node]

    return path[::-1]


def dfs_to_find_path(curr_point, paths, is_visited):
    x, y = curr_point
    for dx, dy in DIRECTION:
        temp_x, temp_y = x + dx, y + dy

        if (temp_x, temp_y) not in paths:
            continue
        if (temp_x, temp_y) in is_visited:
            continue

        is_visited.append((temp_x, temp_y))
        dfs_to_find_path((temp_x, temp_y), paths, is_visited)


n, m, k = list(map(int, input().split()))

input_map = [list(map(int, input().split())) for _ in range(n)]
loc_of_paths = set()
for i in range(n):
    for j in range(n):
        if input_map[i][j] != 0:
            loc_of_paths.add((i, j))

# 군집 좌표 뽑아내기
idx = 0
already_visited = set()
clusters = []
for i in range(n):
    for j in range(n):
        if (i, j) not in already_visited and input_map[i][j] != 0:
            found_path = [(i, j)]
            dfs_to_find_path((i, j), loc_of_paths, found_path)
            already_visited = already_visited | set(found_path)

            clusters.append(Cluster(input_map, idx, found_path[:]))

# Make ball path
ball_path = []
start_loc = [(0, 0)]
for turn in range(4):
    for n_iter in range(n):
        if turn == 0:
            ball_path.append([(n_iter, j) for j in range(n)])
        elif turn == 1:
            ball_path.append([(i, n_iter) for i in range(n - 1, -1, -1)])
        elif turn == 2:
            ball_path.append([(n - n_iter - 1, j) for j in range(n - 1, -1, -1)])
        elif turn == 3:
            ball_path.append([(i, n - n_iter - 1) for i in range(n)])

answer = 0
for k_iter in range(k):
    for c in clusters:
        c.move()

    ball_round = k_iter % len(ball_path)

    for b_path in ball_path[ball_round]:
        catched = False
        for c in clusters:
            ret = c.is_there(b_path)
            if ret != -1:
                answer += ret
                catched = True
                break
        if catched:
            break

    # for i, c in enumerate(clusters):
    #     # if i != 1:
    #     #     continue
    #     print(f"{i}: ")
    #     print(f"\t {c.path_value}")
    #     print(f"\t {c.numbering}")
print(answer)
