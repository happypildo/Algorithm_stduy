from collections import deque
import heapq

MAP_SIZE = 5
DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]
COUNT = []


class Relic:
    def __init__(self, num_of_relics, x, y, r, locs):
        self.num_of_relics = num_of_relics
        self.x = x
        self.y = y
        self.r = r
        self.locs = locs

    def __lt__(self, other):
        if self.num_of_relics > other.num_of_relics:
            return True
        elif self.num_of_relics < other.num_of_relics:
            return False
        if self.r < other.r:
            return True
        elif self.r > other.r:
            return False
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        if self.x < other.x:
            return True
        else:
            return False


class FullingPriority:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        if self.x > other.x:
            return True
        else:
            return False


def bfs_to_search(relic_map, start_point):
    target_val = relic_map[start_point[0]][start_point[1]]

    queue = deque([start_point])
    is_visited = {start_point}

    while queue:
        x, y = queue.popleft()

        for dx, dy in DIRECTION:
            temp_x, temp_y = x + dx, y + dy

            if (-1 < temp_x < MAP_SIZE) and (-1 < temp_y < MAP_SIZE):
                if (temp_x, temp_y) in is_visited:
                    continue
                if relic_map[temp_x][temp_y] != target_val:
                    continue

                queue.append((temp_x, temp_y))
                is_visited.add((temp_x, temp_y))

    return target_val, is_visited


def first_search(relic_map):
    min_heap = []
    for i in range(1, MAP_SIZE - 1):
        for j in range(1, MAP_SIZE - 1):
            for r_iter in range(4):
                partial_relic = [[relic_map[x][y] for y in range(j - 1, j + 2)] for x in range(i - 1, i + 2)]
                # rotated_partial_relic = list(zip(*partial_relic))
                # rotated_partial_relic = [line[::-1] for line in rotated_partial_relic]
                rotated_partial_relic = list(map(list, zip(*partial_relic[::-1])))

                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        relic_map[x][y] = rotated_partial_relic[x - (i - 1)][y - (j - 1)]

                if r_iter == 3:
                    break

                num_of_relics = 0
                relic_locs = set()
                total_visited = set()
                for x in range(MAP_SIZE):
                    for y in range(MAP_SIZE):
                        if (x, y) in total_visited:
                            continue

                        target, visited_result = bfs_to_search(relic_map, (x, y))

                        total_visited = total_visited | visited_result

                        if len(visited_result) >= 3:
                            num_of_relics += len(visited_result)
                            relic_locs = relic_locs | visited_result

                min_heap.append(Relic(len(relic_locs), i, j, r_iter, relic_locs))

    heapq.heapify(min_heap)

    target_relic = min_heap[0]

    i, j = target_relic.x, target_relic.y
    r_iter = target_relic.r

    rotated_partial_relic = [[relic_map[x][y] for y in range(j - 1, j + 2)] for x in range(i - 1, i + 2)]
    for r in range(r_iter + 1):
        rotated_partial_relic = list(zip(*rotated_partial_relic))
        rotated_partial_relic = [line[::-1] for line in rotated_partial_relic]

    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            relic_map[x][y] = rotated_partial_relic[x - (i - 1)][y - (j - 1)]

    return target_relic


def infinitely_search(relic_map, target_relic, num_on_wall):
    this_turn_count = 0

    while True:
        min_heap = []
        this_turn_count += target_relic.num_of_relics
        for point in target_relic.locs:
            min_heap.append(FullingPriority(point[0], point[1]))
        heapq.heapify(min_heap)
        while min_heap:
            FP = heapq.heappop(min_heap)
            i, j = FP.x, FP.y
            relic_map[i][j] = num_on_wall.pop(0)

        num_of_relics = 0
        relic_locs = set()
        total_visited = set()
        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                if (x, y) in total_visited:
                    continue

                target, visited_result = bfs_to_search(relic_map, (x, y))

                total_visited = total_visited | visited_result

                if len(visited_result) >= 3:
                    num_of_relics += len(visited_result)
                    relic_locs = relic_locs | visited_result

        target_relic = Relic(num_of_relics, 0, 0, 0, relic_locs)

        if num_of_relics == 0:
            COUNT.append(this_turn_count)
            return


K, M = list(map(int, input().split()))

relic_numbers = [list(map(int, input().split())) for _ in range(MAP_SIZE)]
wall_numbers = list(map(int, input().split()))

for _ in range(K):
    searched_relic = first_search(relic_numbers)
    infinitely_search(relic_numbers, searched_relic, wall_numbers)

    if COUNT[-1] == 0:
        break

if COUNT[-1] == 0:
    for c in COUNT[:-1]:
        print(c, end=" ")
else:
    for c in COUNT:
        print(c, end=" ")