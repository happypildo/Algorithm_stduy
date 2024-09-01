from collections import deque

DIRECTION = [[-1, 0], [1, 0], [0, -1], [0, 1]]


def BFS(N, input_map, start_node, house, number):
    is_visited = set()
    is_visited.add(start_node)
    queue = deque()
    queue.append(start_node)
    house[number].add(start_node)

    while queue:
        x, y = queue.popleft()

        for dx, dy in DIRECTION:
            if (-1 < x + dx < N) and (-1 < y + dy < N):
                if input_map[x + dx][y + dy] == "0": continue
                if (x+dx, y+dy) in is_visited: continue
                is_visited.add((x+dx, y+dy))
                queue.append((x+dx, y+dy))
                house[number].add((x+dx, y+dy))

    return house, is_visited

N = int(input())
input_map = [input() for _ in range(N)]


is_visited = set()
number = 0
house = {}
for i in range(N):
    for j in range(N):
        if input_map[i][j] == "0": continue
        if (i, j) in is_visited: continue
        number += 1
        house[number] = set()

        house, is_visited_ret = BFS(N, input_map, (i, j), house, number)
        is_visited = is_visited | is_visited_ret

keys = house.keys()
print(len(keys))
answer = sorted([len(house[key]) for key in keys])
for x in answer:
    print(x)

        